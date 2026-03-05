import { useState, useCallback, useEffect } from 'react'
import Scene from './components/Scene'
import ControlPanel from './components/ControlPanel'
import { AIRCRAFT_PARTS } from './config/parts'

function buildInitialVisibility() {
  const vis = {}
  AIRCRAFT_PARTS.forEach(part => {
    vis[part.id] = part.defaultVisible
  })
  return vis
}

export default function App() {
  const [visibility, setVisibility] = useState(buildInitialVisibility)
  const [modelReady, setModelReady] = useState(false)
  const [modelError, setModelError] = useState(false)

  useEffect(() => {
    fetch('/models/a339-corsair.glb', { method: 'HEAD' })
      .then(res => {
        if (res.ok && res.headers.get('content-type') !== 'text/html') {
          setModelReady(true)
        } else {
          setModelError(true)
        }
      })
      .catch(() => setModelError(true))
  }, [])

  const handleToggle = useCallback((partId) => {
    setVisibility(prev => ({
      ...prev,
      [partId]: !prev[partId],
    }))
  }, [])

  const handleShowAll = useCallback(() => {
    setVisibility(prev => {
      const next = { ...prev }
      Object.keys(next).forEach(k => next[k] = true)
      return next
    })
  }, [])

  const handleHideAll = useCallback(() => {
    setVisibility(prev => {
      const next = { ...prev }
      Object.keys(next).forEach(k => next[k] = false)
      return next
    })
  }, [])

  return (
    <div className="w-screen h-screen relative bg-gray-950">
      {modelReady ? (
        <Scene visibility={visibility} />
      ) : (
        <div className="w-full h-full flex items-center justify-center">
          <div className="text-center text-white">
            {modelError ? (
              <>
                <div className="text-6xl mb-6">&#9992;</div>
                <h2 className="text-2xl font-bold mb-3">Modele GLB manquant</h2>
                <p className="text-gray-400 max-w-md leading-relaxed">
                  Le fichier <code className="bg-gray-800 px-2 py-1 rounded text-blue-400">a339-corsair.glb</code> n'a pas ete trouve.
                </p>
                <div className="mt-6 text-left bg-gray-900 rounded-lg p-5 text-sm text-gray-300 max-w-lg">
                  <p className="font-semibold text-white mb-2">Etapes :</p>
                  <ol className="list-decimal list-inside space-y-2">
                    <li>Ouvrir <code className="text-blue-400">A339-corsair.blend</code> dans Blender</li>
                    <li>Onglet <strong>Scripting</strong> → Open → <code className="text-blue-400">export_gltf.py</code></li>
                    <li>Run Script pour lister les objets</li>
                    <li>Ajuster le mapping puis exporter</li>
                    <li>Copier le GLB dans <code className="text-blue-400">viewer/public/models/</code></li>
                  </ol>
                </div>
              </>
            ) : (
              <>
                <div className="animate-spin w-10 h-10 border-4 border-blue-500 border-t-transparent rounded-full mx-auto mb-4" />
                <p className="text-gray-400">Chargement...</p>
              </>
            )}
          </div>
        </div>
      )}
      <ControlPanel
        visibility={visibility}
        onToggle={handleToggle}
        onShowAll={handleShowAll}
        onHideAll={handleHideAll}
      />
    </div>
  )
}
