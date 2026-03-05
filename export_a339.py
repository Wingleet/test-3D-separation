"""
Export A339 Corsair — Séparation en composants pour web viewer
==============================================================
Exécuté en mode headless:
  blender A339-corsair.blend --background --python export_a339.py
"""

import bpy
import os
from collections import defaultdict

OUTPUT_DIR = os.path.dirname(bpy.data.filepath)
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "viewer", "public", "models", "a339-corsair.glb")

# ── Classification spatiale ──────────────────────────────────
# Modèle orienté: X=latéral, Y=vertical, Z=longitudinal (nose=+Z, tail=-Z)
# Fuselage rayon ~110 unités

def classify_piece(cx, cy, cz, sx, sy, sz, verts):
    """Classifie une pièce par sa position spatiale"""
    abs_cx = abs(cx)

    # Radome (nez de l'avion)
    if cz > 1050 and abs_cx < 130:
        return "radome"

    # Plan vertical (rudder) — queue, haut, centré
    if cz < -800 and cy > 350 and abs_cx < 80:
        return "rudder"

    # Plan horizontal (elevator) — queue, mi-hauteur, étendu en X
    if cz < -800 and cy > 200 and abs_cx < 400:
        if cx < -20:
            return "elevator"  # on met tout ensemble
        return "elevator"

    # Trains d'atterrissage — bas de l'avion
    if cy < 50:
        # Nose gear — avant, centré
        if cz > 700 and abs_cx < 80:
            return "gear_nose"
        # Main gear — position des roues principales
        if abs_cx > 100 and abs_cx < 350 and -200 < cz < 200:
            if cx > 0:
                return "gear_main_rh"
            else:
                return "gear_main_lh"

    # Fan blades — dans la zone moteur, petites pièces circulaires
    if 130 < abs_cx < 300 and 0 < cy < 80 and -100 < cz < 150:
        # Les fans sont les pièces avec beaucoup de petits éléments
        if verts < 100 and sy < 5:
            if cx > 0:
                return "fan_rh"
            else:
                return "fan_lh"

    # Moteurs (nacelles) — sous les ailes
    if 130 < abs_cx < 300 and cy < 160 and -100 < cz < 150:
        if cx > 0:
            return "engine_rh"
        else:
            return "engine_lh"

    # Ailes — grande envergure
    if abs_cx > 250:
        if cx > 0:
            return "wing_rh"
        else:
            return "wing_lh"

    # Tout le reste = fuselage
    return "fuselage"


# ── Script principal ─────────────────────────────────────────

print("=" * 60)
print("EXPORT A339 CORSAIR — Séparation en composants")
print("=" * 60)

# 1. Dupliquer l'objet original pour ne pas le modifier
original = bpy.data.objects['A330_900_corsair']
bpy.context.view_layer.objects.active = original
original.select_set(True)
bpy.ops.object.duplicate()
work_obj = bpy.context.active_object
work_obj.name = "WORK_COPY"

# Déselectionner l'original
original.select_set(False)
original.hide_set(True)

print(f"\nCopie de travail créée: {len(work_obj.data.vertices)} vertices")

# 2. Séparer par matériau d'abord
bpy.ops.object.select_all(action='DESELECT')
work_obj.select_set(True)
bpy.context.view_layer.objects.active = work_obj
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.separate(type='MATERIAL')
bpy.ops.object.mode_set(mode='OBJECT')

# 3. Séparer chaque morceau par loose parts
mat_pieces = [o for o in bpy.data.objects if o.type == 'MESH' and o.name.startswith("WORK_COPY")]
print(f"Pièces après séparation par matériau: {len(mat_pieces)}")

all_loose = []
for piece in mat_pieces:
    bpy.ops.object.select_all(action='DESELECT')
    piece.select_set(True)
    bpy.context.view_layer.objects.active = piece
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.separate(type='LOOSE')
    bpy.ops.object.mode_set(mode='OBJECT')

all_pieces = [o for o in bpy.data.objects if o.type == 'MESH' and o.name.startswith("WORK_COPY")]
print(f"Pièces après séparation par loose parts: {len(all_pieces)}")

# 4. Classifier chaque pièce
groups = defaultdict(list)

for obj in all_pieces:
    verts = obj.data.vertices
    if len(verts) == 0:
        continue

    xs = [v.co.x for v in verts]
    ys = [v.co.y for v in verts]
    zs = [v.co.z for v in verts]

    cx = (min(xs) + max(xs)) / 2
    cy = (min(ys) + max(ys)) / 2
    cz = (min(zs) + max(zs)) / 2
    sx = max(xs) - min(xs)
    sy = max(ys) - min(ys)
    sz = max(zs) - min(zs)

    group = classify_piece(cx, cy, cz, sx, sy, sz, len(verts))
    groups[group].append(obj)

print("\n── Classification ──")
for group_name in sorted(groups.keys()):
    pieces = groups[group_name]
    total_verts = sum(len(o.data.vertices) for o in pieces)
    print(f"  {group_name}: {len(pieces)} pièces, {total_verts} vertices")

# 5. Joindre les pièces de chaque groupe
print("\n── Fusion des groupes ──")
final_objects = []

for group_name, pieces in groups.items():
    if not pieces:
        continue

    # Désélectionner tout
    bpy.ops.object.select_all(action='DESELECT')

    # Sélectionner toutes les pièces du groupe
    for p in pieces:
        p.select_set(True)

    # Activer la première pièce
    bpy.context.view_layer.objects.active = pieces[0]

    # Joindre
    if len(pieces) > 1:
        bpy.ops.object.join()

    # Renommer
    joined = bpy.context.active_object
    joined.name = group_name
    final_objects.append(joined)
    print(f"  {group_name}: {len(joined.data.vertices)} vertices")

# 6. Nettoyer — supprimer l'original caché
original.hide_set(False)
bpy.data.objects.remove(original, do_unlink=True)

# 7. Sélectionner uniquement les objets finaux pour l'export
bpy.ops.object.select_all(action='DESELECT')
for obj in final_objects:
    obj.select_set(True)

# 8. Créer le dossier de sortie si nécessaire
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

# 9. Export GLB
print(f"\n── Export GLB ──")
bpy.ops.export_scene.gltf(
    filepath=OUTPUT_FILE,
    export_format='GLB',
    use_selection=True,
    export_apply=True,
    export_texcoords=True,
    export_normals=True,
    export_materials='EXPORT',
    export_image_format='AUTO',
    export_draco_mesh_compression_enable=True,
    export_draco_mesh_compression_level=6,
)

file_size_mb = os.path.getsize(OUTPUT_FILE) / (1024 * 1024)
print(f"\n✅ Export terminé: {OUTPUT_FILE}")
print(f"   Taille: {file_size_mb:.1f} MB")

# Lister les noms des objets dans le GLB
print(f"\n── Objets dans le GLB ──")
for obj in final_objects:
    print(f"  - {obj.name}")

print("\n🎉 Terminé ! Lancez le viewer avec: cd viewer && npm run dev")
