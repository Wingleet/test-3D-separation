import { AIRCRAFT_PARTS, CATEGORIES } from '../config/parts'

export default function ControlPanel({ visibility, onToggle, onShowAll, onHideAll }) {
  return (
    <div className="absolute top-0 right-0 h-full w-80 bg-gray-900/90 backdrop-blur-md text-white p-5 overflow-y-auto z-10 border-l border-gray-700/50">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-lg font-bold tracking-wide">A339 Corsair</h1>
        <p className="text-xs text-gray-400 mt-1">Airbus A330-900neo</p>
      </div>

      {/* Boutons rapides */}
      <div className="flex gap-2 mb-6">
        <button
          onClick={onShowAll}
          className="flex-1 px-3 py-2 bg-blue-600 hover:bg-blue-500 rounded text-sm font-medium transition-colors"
        >
          Tout afficher
        </button>
        <button
          onClick={onHideAll}
          className="flex-1 px-3 py-2 bg-gray-700 hover:bg-gray-600 rounded text-sm font-medium transition-colors"
        >
          Tout masquer
        </button>
      </div>

      {/* Liste par catégorie */}
      {CATEGORIES.map(category => (
        <div key={category} className="mb-5">
          <h2 className="text-xs font-semibold uppercase tracking-wider text-gray-400 mb-2">
            {category}
          </h2>
          <div className="space-y-1">
            {AIRCRAFT_PARTS
              .filter(part => part.category === category)
              .map(part => (
                <label
                  key={part.id}
                  className="flex items-center gap-3 px-3 py-2 rounded hover:bg-gray-800/60 cursor-pointer transition-colors group"
                >
                  <input
                    type="checkbox"
                    checked={visibility[part.id] ?? true}
                    onChange={() => onToggle(part.id)}
                    className="w-4 h-4 rounded border-gray-500 text-blue-500 focus:ring-blue-500 focus:ring-offset-0 bg-gray-700 cursor-pointer"
                  />
                  <span className="text-sm group-hover:text-white text-gray-300 transition-colors">
                    {part.label}
                  </span>
                  <span
                    className={`ml-auto w-2 h-2 rounded-full transition-colors ${
                      visibility[part.id] ? 'bg-green-400' : 'bg-gray-600'
                    }`}
                  />
                </label>
              ))}
          </div>
        </div>
      ))}

      {/* Footer */}
      <div className="mt-6 pt-4 border-t border-gray-700/50 text-xs text-gray-500">
        Cliquez sur les cases pour afficher/masquer les composants
      </div>
    </div>
  )
}
