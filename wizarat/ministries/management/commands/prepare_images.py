import json
import re
import sys
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from PIL import Image, ImageOps


GALLERY_EXTENSIONS = {".jpg", ".jpeg", ".jfif", ".webp", ".png"}
WEBP_WIDTHS = (640, 1280, 1920)


class Command(BaseCommand):
    help = "Prepare responsive ministry cover and gallery images."

    def handle(self, *args, **options):
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")

        project_dir = Path(__file__).resolve().parents[3]
        app_dir = Path(__file__).resolve().parents[2]
        source_dir = project_dir / "image_sources"
        image_map_path = app_dir / "data" / "images.json"
        output_root = app_dir / "static" / "ministries" / "images"

        try:
            image_map = json.loads(image_map_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise CommandError(f"Unable to read image mapping {image_map_path}: {error}") from error

        if not isinstance(image_map, dict) or not image_map:
            raise CommandError("The image mapping must be a non-empty JSON object.")

        output_root.mkdir(parents=True, exist_ok=True)
        total_outputs = 0
        incomplete = False

        for slug, mapping in image_map.items():
            if not isinstance(mapping, dict) or not isinstance(mapping.get("gallery"), list):
                raise CommandError(f"Invalid image mapping for ministry '{slug}'.")

            ministry_dir = output_root / slug
            ministry_dir.mkdir(parents=True, exist_ok=True)
            self._remove_generated_files(ministry_dir)

            self.stdout.write(f"\n[{slug}]")
            source_cover = self._find_cover(source_dir, mapping.get("cover", ""))
            gallery_sources = [
                self._find_gallery_image(source_dir, stem)
                for stem in mapping["gallery"]
            ]
            found = [path for path in [source_cover, *gallery_sources] if path is not None]
            missing = []

            if source_cover is None:
                missing.append(f"cover: {mapping.get('cover', '(not mapped)')}")
            missing.extend(
                f"gallery: {stem}"
                for stem, path in zip(mapping["gallery"], gallery_sources)
                if path is None
            )
            self.stdout.write(
                "  Found: " + (", ".join(path.name for path in found) if found else "none")
            )
            if missing:
                incomplete = True
                self.stdout.write(self.style.WARNING("  Missing: " + ", ".join(missing)))

            cover_image = None
            if source_cover is not None:
                cover_image = self._open_rgb(source_cover)
                total_outputs += self._write_cover(cover_image, ministry_dir)

            gallery_index = 0
            for source_path in gallery_sources:
                if source_path is None:
                    continue
                gallery_index += 1
                gallery_image = self._open_rgb(source_path)
                total_outputs += self._write_gallery_image(
                    gallery_image,
                    ministry_dir,
                    gallery_index,
                )
                gallery_image.close()

            if cover_image is not None:
                gallery_index += 1
                total_outputs += self._write_gallery_cover(
                    cover_image,
                    ministry_dir,
                    gallery_index,
                )
                cover_image.close()

            output_files = sorted(
                (path for path in ministry_dir.iterdir() if path.is_file()),
                key=lambda path: path.name,
            )
            if output_files:
                self.stdout.write("  Final files:")
                for output_path in output_files:
                    with Image.open(output_path) as output_image:
                        dimensions = f"{output_image.width}x{output_image.height}"
                    size_kb = output_path.stat().st_size / 1024
                    self.stdout.write(
                        f"    {output_path.name}: {dimensions}, {size_kb:.1f} KB"
                    )
            else:
                incomplete = True
                self.stdout.write(self.style.WARNING("  Final files: none"))

            if gallery_index < 2:
                incomplete = True
                self.stdout.write(
                    self.style.WARNING(
                        "  Warning: fewer than two gallery images; a gallery source is missing."
                    )
                )

        self.stdout.write(
            f"\nPrepared {total_outputs} image files across {len(image_map)} ministries."
        )
        if incomplete:
            self.stdout.write(
                self.style.WARNING(
                    "Some source images are missing. Add them to image_sources and rerun this command."
                )
            )

    @staticmethod
    def _find_cover(source_dir, filename):
        if not filename:
            return None
        candidate = source_dir / filename
        return candidate if candidate.is_file() else None

    @staticmethod
    def _find_gallery_image(source_dir, stem):
        if not stem or not source_dir.is_dir():
            return None
        normalized_stem = stem.casefold()
        matches = sorted(
            (
                path
                for path in source_dir.iterdir()
                if path.is_file()
                and path.suffix.casefold() in GALLERY_EXTENSIONS
                and path.stem.casefold() == normalized_stem
            ),
            key=lambda path: path.name.casefold(),
        )
        return matches[0] if matches else None

    @staticmethod
    def _open_rgb(source_path):
        try:
            with Image.open(source_path) as source_image:
                return ImageOps.exif_transpose(source_image).convert("RGB")
        except (OSError, ValueError) as error:
            raise CommandError(f"Unable to process image {source_path}: {error}") from error

    @staticmethod
    def _bounded_copy(image, max_width):
        result = image.copy()
        if result.width > max_width:
            height = round(result.height * max_width / result.width)
            result = result.resize(
                (max_width, height),
                Image.Resampling.LANCZOS,
            )
        return result

    def _write_cover(self, image, ministry_dir):
        outputs = 0
        cover_jpg = self._bounded_copy(image, 1600)
        try:
            cover_jpg.save(
                ministry_dir / "cover.jpg",
                format="JPEG",
                quality=82,
                optimize=True,
                progressive=True,
            )
        finally:
            cover_jpg.close()
        outputs += 1

        widths = self._output_widths(image.width)
        for width in widths:
            webp_image = self._bounded_copy(image, width)
            try:
                webp_image.save(
                    ministry_dir / f"cover-{width}.webp",
                    format="WEBP",
                    quality=82,
                    method=6,
                )
            finally:
                webp_image.close()
            outputs += 1
        return outputs

    def _write_gallery_image(self, image, ministry_dir, index):
        outputs = 0
        jpg_path = ministry_dir / f"{index}.jpg"
        image.save(
            jpg_path,
            format="JPEG",
            quality=90,
            optimize=True,
            progressive=True,
        )
        outputs += 1

        for width in self._output_widths(image.width):
            webp_image = self._bounded_copy(image, width)
            try:
                webp_image.save(
                    ministry_dir / f"{index}-{width}.webp",
                    format="WEBP",
                    quality=82,
                    method=6,
                )
            finally:
                webp_image.close()
            outputs += 1
        return outputs

    def _write_gallery_cover(self, image, ministry_dir, index):
        gallery_cover = self._bounded_copy(image, 1600)
        try:
            gallery_cover.save(
                ministry_dir / f"{index}.jpg",
                format="JPEG",
                quality=82,
                optimize=True,
                progressive=True,
            )
        finally:
            gallery_cover.close()
        outputs = 1

        for width in self._output_widths(image.width):
            webp_image = self._bounded_copy(image, width)
            try:
                webp_image.save(
                    ministry_dir / f"{index}-{width}.webp",
                    format="WEBP",
                    quality=82,
                    method=6,
                )
            finally:
                webp_image.close()
            outputs += 1
        return outputs

    @staticmethod
    def _output_widths(source_width):
        return WEBP_WIDTHS

    @staticmethod
    def _remove_generated_files(ministry_dir):
        generated_name = re.compile(r"(?:cover|\d+)(?:-\d+)?\.(?:jpg|webp)$", re.IGNORECASE)
        for path in ministry_dir.iterdir():
            if path.is_file() and generated_name.fullmatch(path.name):
                path.unlink()
