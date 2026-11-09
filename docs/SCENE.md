# Relief map

The homepage renders the vector map with six destination links overlaid in HTML. Selecting **3D map** fetches the Three.js module, builds a relief from the same Natural Earth mainland outline and displays the canvas after the first frame renders. The relief height and marker locations are illustrative. The rings on the land mark examples of ROSHN’s communities.

The scene uses an orthographic camera, layered coastal edges, a height field with contour lines, and soft directional and hemisphere lighting. The relief projects each HTML label onto the scene so the same links work with a keyboard, pointer or touchscreen in either view. [Three.js WebGLRenderer](https://threejs.org/docs/pages/WebGLRenderer.html) · [OrthographicCamera](https://threejs.org/docs/pages/OrthographicCamera.html)

Resize schedules frames while the stage is visible. There is no continuous render loop. Device pixel ratio is capped at 1.5. Closing the view, leaving the page or turning on reduced motion removes the canvas and releases GPU resources. Reduced motion keeps the poster and links. Failed imports, unavailable WebGL 2 and lost contexts restore the poster and announce a localized status.

Vite defers Three.js until the relief map opens. Three.js ships under the [MIT license](licenses/three-MIT.txt). The boundary source and geographic references are recorded in [SOURCES.md](SOURCES.md#map-geography).
