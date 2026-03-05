/**
 * Configuration des pièces de l'A339 Corsair
 *
 * - id: identifiant interne (doit matcher le nom du node dans le glTF)
 * - label: nom affiché dans l'interface
 * - category: groupe pour l'affichage dans le panneau
 * - defaultVisible: état initial
 */
export const AIRCRAFT_PARTS = [
  { id: 'fuselage', label: 'Fuselage', category: 'Structure', defaultVisible: true },
  { id: 'wing_lh', label: 'Aile LH (#1)', category: 'Structure', defaultVisible: true },
  { id: 'wing_rh', label: 'Aile RH (#2)', category: 'Structure', defaultVisible: true },
  { id: 'engine_lh', label: 'Réacteur LH (#1)', category: 'Motorisation', defaultVisible: true },
  { id: 'engine_rh', label: 'Réacteur RH (#2)', category: 'Motorisation', defaultVisible: true },
  { id: 'fan_lh', label: 'FAN Engine LH (#1)', category: 'Motorisation', defaultVisible: true },
  { id: 'fan_rh', label: 'FAN Engine RH (#2)', category: 'Motorisation', defaultVisible: true },
  { id: 'elevator', label: 'Plan horizontal (Elevator)', category: 'Empennage', defaultVisible: true },
  { id: 'rudder', label: 'Plan vertical (Rudder)', category: 'Empennage', defaultVisible: true },
  { id: 'radome', label: 'Radome', category: 'Structure', defaultVisible: true },
  { id: 'gear_main_lh', label: 'Train principal LH', category: 'Trains', defaultVisible: true },
  { id: 'gear_main_rh', label: 'Train principal RH', category: 'Trains', defaultVisible: true },
  { id: 'gear_nose', label: 'Train avant (Nose)', category: 'Trains', defaultVisible: true },
]

export const CATEGORIES = [...new Set(AIRCRAFT_PARTS.map(p => p.category))]
