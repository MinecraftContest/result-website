/* global THREE, fetch */
const { WorldView, Viewer, MapControls } = require('prismarine-viewer/viewer')
const { Vec3 } = require('vec3')
const { Schematic } = require('prismarine-schematic')
const Chunk = require('prismarine-chunk')('1.17.1')
global.THREE = require('three')

function generateEmptyChunk(chunkX, chunkZ) {
  const chunk = new Chunk()
  return chunk
}

async function main () {
  const version = '1.17.1'

  const url = new URL(window.location.href)

  const data = await fetch('data/models/' + url.searchParams.get('model') + '.schem').then(r => r.arrayBuffer())
  const schem = await Schematic.read(Buffer.from(data), version)

  const viewDistance = 10

  const width = Math.abs(schem.end().x - schem.start().x)
  const length = Math.abs(schem.end().z - schem.start().z)

  const center = new Vec3(width * 0.5, 0, -1 * length * 0.5)
  const cameraPosition = new Vec3(width * 0.75, 75, -1 * length * 0.75)

  console.log(center)

  const World = require('prismarine-world')(version)

  const world = new World(generateEmptyChunk)

  await schem.paste(world, new Vec3(0, 60, 0))

  const worldView = new WorldView(world, viewDistance, center)

  // Create three.js context, add to page
  const renderer = new THREE.WebGLRenderer()
  renderer.setPixelRatio(window.devicePixelRatio || 1)
  renderer.setSize(window.innerWidth, window.innerHeight)
  document.body.appendChild(renderer.domElement)

  // Create viewer
  const viewer = new Viewer(renderer)
  viewer.setVersion(version)
  // Attach controls to viewer
  const controls = new MapControls(viewer.camera, renderer.domElement)

  // Link WorldView and Viewer
  viewer.listen(worldView)
  // Initialize viewer, load chunks
  worldView.init(center)

  viewer.camera.position.set(cameraPosition.x, cameraPosition.y, cameraPosition.z)
  controls.target.set(center.x, center.y, center.z)

  const spinner = document.getElementById('loading-spinner')
  spinner.parentElement.removeChild(spinner)

  // Browser animation loop
  const animate = () => {
    window.requestAnimationFrame(animate)
    if (controls) controls.update()
    worldView.updatePosition(controls.target)
    viewer.update()
    renderer.render(viewer.scene, viewer.camera)
  }
  animate()
}
main()
