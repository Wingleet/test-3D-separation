"""
Script Blender — Export A339 Corsair en GLB pour web viewer
============================================================
Usage:
  1. Ouvrir A339-corsair.blend dans Blender
  2. Aller dans Scripting > Open > export_gltf.py
  3. Lancer le script (Run Script)

Le script va:
  - Phase 1: Lister tous les objets de la scène (pour vérifier le mapping)
  - Phase 2: Organiser les objets en collections nommées
  - Phase 3: Exporter en GLB optimisé pour le web
"""

import bpy
import os

# === CONFIGURATION ===

# Dossier de sortie pour le GLB
OUTPUT_DIR = os.path.dirname(bpy.data.filepath)
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "a339-corsair.glb")

# Mapping: nom interne → objets Blender (à ajuster après Phase 1)
# Les clés sont les identifiants utilisés dans l'app web
# Les valeurs sont des listes de mots-clés pour matcher les noms d'objets Blender
PART_KEYWORDS = {
    "fuselage": ["fuselage", "fuse", "body"],
    "wing_rh": ["wing_rh", "wing_r", "aile_d", "wing.r", "wing.002"],
    "wing_lh": ["wing_lh", "wing_l", "aile_g", "wing.l", "wing.001"],
    "engine_rh": ["engine_rh", "engine_r", "nacelle_r", "engine.r", "nacelle.002", "reacteur_d"],
    "engine_lh": ["engine_lh", "engine_l", "nacelle_l", "engine.l", "nacelle.001", "reacteur_g"],
    "fan_rh": ["fan_rh", "fan_r", "blade_r", "fan.r", "fan.002"],
    "fan_lh": ["fan_lh", "fan_l", "blade_l", "fan.l", "fan.001"],
    "elevator": ["elevator", "horizontal", "stabilizer", "htp", "h_stab", "tailplane"],
    "rudder": ["rudder", "vertical", "fin", "vtp", "v_stab", "vertical_stab"],
    "radome": ["radome", "nose_cone", "radar"],
    "gear_main_lh": ["gear_main_l", "main_gear_l", "mlg_l", "landing_l", "train_g"],
    "gear_main_rh": ["gear_main_r", "main_gear_r", "mlg_r", "landing_r", "train_d"],
    "gear_nose": ["gear_nose", "nose_gear", "nlg", "nose_land", "train_av"],
}


def phase1_list_objects():
    """Phase 1: Lister tous les objets MESH de la scène"""
    print("\n" + "=" * 60)
    print("PHASE 1 — LISTE DES OBJETS DE LA SCÈNE")
    print("=" * 60)

    meshes = [obj for obj in bpy.data.objects if obj.type == 'MESH']
    print(f"\nNombre total d'objets MESH: {len(meshes)}\n")

    # Lister par collection
    for col in bpy.data.collections:
        col_objects = [obj for obj in col.objects if obj.type == 'MESH']
        if col_objects:
            print(f"\n📁 Collection: {col.name}")
            for obj in sorted(col_objects, key=lambda o: o.name):
                verts = len(obj.data.vertices) if obj.data else 0
                print(f"   ├─ {obj.name} ({verts} vertices)")

    # Objets hors collection
    scene_col = bpy.context.scene.collection
    root_objects = [obj for obj in scene_col.objects if obj.type == 'MESH']
    if root_objects:
        print(f"\n📁 Scene Collection (racine)")
        for obj in sorted(root_objects, key=lambda o: o.name):
            verts = len(obj.data.vertices) if obj.data else 0
            print(f"   ├─ {obj.name} ({verts} vertices)")

    print("\n" + "=" * 60)
    print("Vérifiez les noms ci-dessus et ajustez PART_KEYWORDS si besoin")
    print("puis relancez le script pour la Phase 2 + 3")
    print("=" * 60)

    return meshes


def match_part(obj_name):
    """Trouve à quel groupe appartient un objet basé sur son nom"""
    name_lower = obj_name.lower()
    for part_id, keywords in PART_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in name_lower:
                return part_id
    return None


def phase2_organize():
    """Phase 2: Créer des collections organisées et y placer les objets"""
    print("\n" + "=" * 60)
    print("PHASE 2 — ORGANISATION DES OBJETS")
    print("=" * 60)

    meshes = [obj for obj in bpy.data.objects if obj.type == 'MESH']

    matched = {}
    unmatched = []

    for obj in meshes:
        part = match_part(obj.name)
        if part:
            if part not in matched:
                matched[part] = []
            matched[part].append(obj)
        else:
            unmatched.append(obj)

    print(f"\nObjets matchés: {sum(len(v) for v in matched.values())}")
    for part_id, objs in sorted(matched.items()):
        print(f"  ✅ {part_id}: {[o.name for o in objs]}")

    if unmatched:
        print(f"\n⚠️  Objets NON matchés ({len(unmatched)}):")
        for obj in unmatched:
            print(f"  ❌ {obj.name}")
        print("\n→ Ajoutez des mots-clés dans PART_KEYWORDS pour ces objets")

    # Renommer les objets parents pour le glTF
    # On utilise des Empty comme parents de groupe
    for part_id, objs in matched.items():
        # Créer un Empty parent pour le groupe
        empty = bpy.data.objects.get(part_id)
        if not empty:
            empty = bpy.data.objects.new(part_id, None)
            bpy.context.scene.collection.objects.link(empty)

        for obj in objs:
            # Garder la transform world avant de re-parenter
            world_matrix = obj.matrix_world.copy()
            obj.parent = empty
            obj.matrix_world = world_matrix

    # Les objets non matchés sont regroupés sous "other"
    if unmatched:
        other_empty = bpy.data.objects.get("other")
        if not other_empty:
            other_empty = bpy.data.objects.new("other", None)
            bpy.context.scene.collection.objects.link(other_empty)
        for obj in unmatched:
            world_matrix = obj.matrix_world.copy()
            obj.parent = other_empty
            obj.matrix_world = world_matrix

    return matched, unmatched


def phase3_export():
    """Phase 3: Exporter en GLB"""
    print("\n" + "=" * 60)
    print("PHASE 3 — EXPORT GLB")
    print("=" * 60)

    # Sélectionner tous les objets mesh
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.data.objects:
        if obj.type in ('MESH', 'EMPTY'):
            obj.select_set(True)

    # Export glTF/GLB
    bpy.ops.export_scene.gltf(
        filepath=OUTPUT_FILE,
        export_format='GLB',
        use_selection=False,
        export_apply=True,
        export_texcoords=True,
        export_normals=True,
        export_colors=True,
        export_materials='EXPORT',
        export_image_format='AUTO',
        export_draco_mesh_compression_enable=True,
        export_draco_mesh_compression_level=6,
    )

    file_size_mb = os.path.getsize(OUTPUT_FILE) / (1024 * 1024)
    print(f"\n✅ Export terminé: {OUTPUT_FILE}")
    print(f"   Taille: {file_size_mb:.1f} MB")
    print(f"\n→ Copiez ce fichier dans viewer/public/models/")


# === EXÉCUTION ===

# Phase 1: toujours exécutée pour voir les objets
all_meshes = phase1_list_objects()

# Phase 2 + 3: décommenter quand le mapping est validé
# matched, unmatched = phase2_organize()
# phase3_export()

print("\n💡 Pour exporter:")
print("   1. Vérifiez le mapping PART_KEYWORDS avec les noms listés ci-dessus")
print("   2. Décommentez les lignes Phase 2 + 3 en bas du script")
print("   3. Relancez le script")
