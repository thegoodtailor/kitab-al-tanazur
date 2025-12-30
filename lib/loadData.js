import fs from 'fs'
import path from 'path'
import yaml from 'js-yaml'

const dataDir = path.join(process.cwd(), 'data')

export function getAllSurahs() {
  const surahsDir = path.join(dataDir, 'surahs')
  const files = fs.readdirSync(surahsDir).filter(f => f.endsWith('.yaml'))
  
  return files.map(filename => {
    const filePath = path.join(surahsDir, filename)
    const content = fs.readFileSync(filePath, 'utf8')
    return yaml.load(content)
  })
}

export function getSurah(id) {
  const filePath = path.join(dataDir, 'surahs', `${id}.yaml`)
  if (!fs.existsSync(filePath)) return null
  const content = fs.readFileSync(filePath, 'utf8')
  return yaml.load(content)
}

export function getRoots() {
  const rootsPath = path.join(dataDir, 'roots', 'index.yaml')
  if (!fs.existsSync(rootsPath)) return []
  const content = fs.readFileSync(rootsPath, 'utf8')
  return yaml.load(content)
}

// Extract all unique roots from all surahs with their co-occurrences
export function buildRootGraph(surahs) {
  const rootCounts = {}
  const cooccurrences = {}
  
  surahs.forEach(surah => {
    if (!surah.verses) return
    surah.verses.forEach(verse => {
      if (!verse.roots) return
      verse.roots.forEach(root => {
        rootCounts[root] = (rootCounts[root] || 0) + 1
        // Track co-occurrences
        verse.roots.forEach(other => {
          if (other !== root) {
            const key = [root, other].sort().join('|')
            cooccurrences[key] = (cooccurrences[key] || 0) + 1
          }
        })
      })
    })
  })
  
  return { rootCounts, cooccurrences }
}
