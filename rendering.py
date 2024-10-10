import numpy as np
import pyrender
import trimesh

def setup_scene():
    scene = pyrender.Scene()

    # Criar um cubo como modelo 3D
    mesh = pyrender.Mesh.from_trimesh(trimesh.creation.box(extents=(1, 1, 1)))
    scene.add(mesh)

    # Configurar a câmera
    camera = pyrender.PerspectiveCamera(yfov=np.pi / 3.0)
    camera_pose = np.array([
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, -1.0],
        [0.0, 0.0, 1.0, 1.0],
        [0.0, 0.0, 0.0, 1.0],
    ])
    scene.add(camera, pose=camera_pose)

    # Adicionar luz
    light = pyrender.DirectionalLight(color=np.ones(3), intensity=2.0)
    scene.add(light, pose=camera_pose)

    renderer = pyrender.OffscreenRenderer(800, 600)
    return scene, renderer

def render_scene(scene, renderer):
    color, _ = renderer.render(scene)
    return color
