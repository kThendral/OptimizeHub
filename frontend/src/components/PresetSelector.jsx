// Location: frontend/src/components/PresetSelector.jsx

import { useState } from 'react';
import { OPTIMIZATION_PRESETS, getDifficultyColor } from '../data/presets';

/**
 * Preset selector component for quick-start optimization scenarios.
 * Allows users to choose from pre-configured optimization examples.
 */
export default function PresetSelector({ onSelectPreset }) {
  const [selectedPreset, setSelectedPreset] = useState('');

  const handlePresetChange = (presetId) => {
    setSelectedPreset(presetId);
    if (presetId && onSelectPreset) {
      const preset = OPTIMIZATION_PRESETS[presetId];
      onSelectPreset(preset);
    }
  };

  return (
    <div className="p-5 bg-gradient-to-r from-purple-50 to-blue-50 rounded-xl border-2 border-purple-200 shadow-sm">
      <div className="flex items-center gap-2 mb-3">
        <span className="text-2xl">🚀</span>
        <h3 className="text-lg font-bold text-gray-800">Quick Start Presets</h3>
        <span className="text-xs bg-purple-200 text-purple-700 px-2 py-1 rounded-full font-semibold">
          NEW
        </span>
      </div>
      
      <p className="text-sm text-gray-600 mb-4">
        New to optimization? Choose a pre-configured scenario below and we'll explain everything:
      </p>

      {/* Preset Dropdown */}
      <select
        value={selectedPreset}
        onChange={e => handlePresetChange(e.target.value)}
        className="w-full p-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500 bg-white text-sm font-medium shadow-sm"
      >
        <option value="">--Choose a Preset Scenario--</option>
        
        {/* Beginner Presets */}
        <optgroup label="🟢 Beginner (Great for Learning)">
          {Object.values(OPTIMIZATION_PRESETS)
            .filter(p => p.difficulty === 'beginner')
            .map(preset => (
              <option key={preset.id} value={preset.id}>
                {preset.name}
              </option>
            ))}
        </optgroup>

        {/* Intermediate Presets */}
        <optgroup label="🟡 Intermediate (More Complex)">
          {Object.values(OPTIMIZATION_PRESETS)
            .filter(p => p.difficulty === 'intermediate')
            .map(preset => (
              <option key={preset.id} value={preset.id}>
                {preset.name}
              </option>
            ))}
        </optgroup>

        {/* Advanced Presets */}
        <optgroup label="🔴 Advanced (Challenging)">
          {Object.values(OPTIMIZATION_PRESETS)
            .filter(p => p.difficulty === 'advanced')
            .map(preset => (
              <option key={preset.id} value={preset.id}>
                {preset.name}
              </option>
            ))}
        </optgroup>
      </select>

      {/* Helper Text */}
      {!selectedPreset && (
        <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-lg text-sm text-blue-700">
          <div className="flex gap-2">
            <span>💡</span>
            <div>
              <strong>Tip:</strong> Each preset includes a detailed explanation of the problem, 
              expected results, and why we chose specific parameters. Perfect for learning!
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
