# Relief map

The homepage renders the illustrated poster and the six destination links in HTML. Selecting **3D map** fetches the Three.js module, builds a relief from the poster’s schematic outline and displays the canvas after the first frame renders. The terrain and point positions are editorial illustrations. The diamond marked `04` identifies ROSHN’s distributed communities. The rings on the land indicate that spread schematically.

The scene uses an orthographic camera, layered coastal edges, a height field with contour lines, and soft directional and hemisphere lighting. It has no downloaded models or textures. The numbered badges are drawn on demand, match the project link numbers and lead to the same localized routes. Keyboard focus on a project link highlights its corresponding badge when the scene is open. [Three.js WebGLRenderer](https://threejs.org/docs/pages/WebGLRenderer.html) · [OrthographicCamera](https://threejs.org/docs/pages/OrthographicCamera.html)

Resize and marker interactions schedule frames while the stage is visible. There is no continuous render loop. Device pixel ratio is capped at 1.5. Closing the view, leaving the page or turning on reduced motion removes the canvas and releases GPU resources. Reduced motion keeps the poster and links. Failed imports, unavailable WebGL 2 and lost contexts restore the poster and announce a localized status.

The production Vite build emits the relief as a deferred chunk of about 559 kB minified and 140 kB gzip. See `docs/EVIDENCE.md` for measured browser transfer and verification results. Three.js ships under the [MIT license](licenses/three-MIT.txt). The poster and relief are original artwork for this atlas.
