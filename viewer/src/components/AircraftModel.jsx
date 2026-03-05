import { useEffect, useRef } from 'react'
import { useGLTF } from '@react-three/drei'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

export default function AircraftModel({ visibility }) {
  const { scene } = useGLTF('/models/a339-corsair.glb')
  const groupRef = useRef()
  const opacityRefs = useRef({})

  useEffect(() => {
    // Parcourir tous les nodes du modèle
    scene.traverse((child) => {
      if (child.isMesh) {
        // Rendre les matériaux transparents pour le fade
        if (Array.isArray(child.material)) {
          child.material = child.material.map(m => {
            const mat = m.clone()
            mat.transparent = true
            return mat
          })
        } else {
          child.material = child.material.clone()
          child.material.transparent = true
        }
      }
    })
  }, [scene])

  useFrame(() => {
    // Animer l'opacité pour un fade smooth
    scene.traverse((child) => {
      // Trouver le parent "group" (Empty dans Blender)
      const partId = findPartId(child)
      if (!partId) return

      const targetOpacity = visibility[partId] ? 1 : 0
      const currentOpacity = opacityRefs.current[child.uuid] ?? 1

      // Interpolation smooth
      const newOpacity = THREE.MathUtils.lerp(currentOpacity, targetOpacity, 0.1)
      opacityRefs.current[child.uuid] = newOpacity

      if (child.isMesh) {
        const materials = Array.isArray(child.material) ? child.material : [child.material]
        materials.forEach(mat => {
          mat.opacity = newOpacity
        })
        child.visible = newOpacity > 0.01
      }
    })
  })

  return (
    <group ref={groupRef}>
      <primitive object={scene} />
    </group>
  )
}

/**
 * Remonte l'arbre des parents pour trouver un node
 * dont le nom correspond à un part ID
 */
function findPartId(node) {
  let current = node
  while (current) {
    if (current.name && isKnownPart(current.name)) {
      return current.name
    }
    current = current.parent
  }
  return null
}

function isKnownPart(name) {
  const parts = [
    'fuselage', 'wing_rh', 'wing_lh',
    'engine_rh', 'engine_lh', 'fan_rh', 'fan_lh',
    'elevator', 'rudder', 'radome',
    'gear_main_lh', 'gear_main_rh', 'gear_nose',
  ]
  return parts.includes(name)
}

useGLTF.preload('/models/a339-corsair.glb')
