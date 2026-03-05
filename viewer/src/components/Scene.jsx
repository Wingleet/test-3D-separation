import { Canvas } from '@react-three/fiber'
import { OrbitControls, Environment, ContactShadows } from '@react-three/drei'
import { Suspense } from 'react'
import AircraftModel from './AircraftModel'

function Loader() {
  return (
    <mesh>
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial color="#444" wireframe />
    </mesh>
  )
}

export default function Scene({ visibility }) {
  return (
    <Canvas
      camera={{ position: [30, 15, 30], fov: 45, near: 0.1, far: 1000 }}
      style={{ width: '100%', height: '100%' }}
      gl={{ antialias: true, alpha: true }}
    >
      <color attach="background" args={['#1a1a2e']} />

      {/* Éclairage */}
      <ambientLight intensity={0.4} />
      <directionalLight position={[10, 20, 10]} intensity={1} castShadow />
      <directionalLight position={[-10, 10, -10]} intensity={0.3} />

      {/* Environnement HDR pour les reflets */}
      <Environment preset="city" />

      {/* Ombres au sol */}
      <ContactShadows
        position={[0, -2, 0]}
        opacity={0.4}
        scale={80}
        blur={2}
        far={20}
      />

      {/* Modèle */}
      <Suspense fallback={<Loader />}>
        <AircraftModel visibility={visibility} />
      </Suspense>

      {/* Contrôles orbitaux */}
      <OrbitControls
        makeDefault
        enablePan
        enableZoom
        enableRotate
        minDistance={5}
        maxDistance={200}
        target={[0, 0, 0]}
      />

      {/* Grille de référence */}
      <gridHelper args={[100, 50, '#333', '#222']} position={[0, -2, 0]} />
    </Canvas>
  )
}
