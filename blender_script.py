import bpy
import os
import sys

# Obter os caminhos do arquivo Blender e do arquivo de áudio da linha de comando
blend_file_path = sys.argv[-2]
audio_file_path = sys.argv[-1]

# Função para carregar o arquivo Blender
def load_blend_file(filepath):
    bpy.ops.wm.open_mainfile(filepath=filepath)

# Função para animar a cabeça
def animate_head():
    bpy.context.scene.frame_start = 0
    bpy.context.scene.frame_end = 250

    # Supondo que o osso da cabeça é chamado 'head_bone'
    head_bone = bpy.data.objects['Armature'].pose.bones['head_bone']
    head_bone.rotation_mode = 'XYZ'

    # Adicionando keyframes para a animação da cabeça
    head_bone.rotation_euler = (0, 0, 0)
    head_bone.keyframe_insert(data_path="rotation_euler", frame=0)
    head_bone.rotation_euler = (0.1, 0, 0)
    head_bone.keyframe_insert(data_path="rotation_euler", frame=50)
    head_bone.rotation_euler = (-0.1, 0, 0)
    head_bone.keyframe_insert(data_path="rotation_euler", frame=100)
    head_bone.rotation_euler = (0.1, 0, 0)
    head_bone.keyframe_insert(data_path="rotation_euler", frame=150)
    head_bone.rotation_euler = (0, 0, 0)
    head_bone.keyframe_insert(data_path="rotation_euler", frame=200)

# Função para simular a respiração
def simulate_breathing():
    bpy.context.scene.frame_start = 0
    bpy.context.scene.frame_end = 250

    # Supondo que o osso do peito é chamado 'chest_bone'
    chest_bone = bpy.data.objects['Armature'].pose.bones['chest_bone']
    chest_bone.scale = (1, 1, 1)
    chest_bone.keyframe_insert(data_path="scale", frame=0)
    chest_bone.scale = (1.1, 1.1, 1.1)
    chest_bone.keyframe_insert(data_path="scale", frame=50)
    chest_bone.scale = (1, 1, 1)
    chest_bone.keyframe_insert(data_path="scale", frame=100)
    chest_bone.scale = (1.1, 1.1, 1.1)
    chest_bone.keyframe_insert(data_path="scale", frame=150)
    chest_bone.scale = (1, 1, 1)
    chest_bone.keyframe_insert(data_path="scale", frame=200)

# Função para adicionar o áudio e sincronizar com a animação
def add_audio(audio_file):
    bpy.ops.sequencer.sound_strip_add(filepath=audio_file, frame_start=1)
    bpy.context.scene.frame_end = bpy.context.scene.sequence_editor.sequences_all[-1].frame_final_end

# Carregar o arquivo Blender
load_blend_file(blend_file_path)

# Animar a cabeça
animate_head()

# Simular respiração
simulate_breathing()

# Adicionar áudio
add_audio(audio_file_path)

# Renderizar a animação
output_path = os.path.dirname(audio_file_path)
bpy.context.scene.render.filepath = os.path.join(output_path, 'animation')
bpy.ops.render.render(animation=True)
