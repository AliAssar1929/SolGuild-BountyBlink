<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as maplibregl from 'maplibre-gl'

const props = defineProps<{
  tasks: Array<{
    id: string
    title: string
    latitude: number
    longitude: number
    reward_sol: number
  }>
  selectedTask: {
    id: string
    latitude: number
    longitude: number
    reward_sol: number
  } | null
}>()

const emit = defineEmits<{
  (e: 'selectTask', task: any): void
}>()

const mapContainer = ref<HTMLDivElement | null>(null)
let map: maplibregl.Map | null = null
let markers: maplibregl.Marker[] = []

const initMap = () => {
  if (!mapContainer.value) return

  // Using free OpenStreetMap raster tiles through MapLibre without default bouncing
  map = new maplibregl.Map({
    container: mapContainer.value,
    attributionControl: false, // Prevents default maplibregl attribution control from mounting
    dragRotate: false,
    pitchWithRotate: false,
    style: {
      version: 8,
      sources: {
        'osm-tiles': {
          type: 'raster',
          tiles: [
            'https://tile.openstreetmap.org/{z}/{x}/{y}.png'
          ],
          tileSize: 256
        }
      },
      layers: [
        {
          id: 'osm-tiles-layer',
          type: 'raster',
          source: 'osm-tiles',
          minzoom: 0,
          maxzoom: 19
        }
      ]
    },
    center: [13.4050, 52.5200], // Berlin center
    zoom: 13
  })

  // Immediate JS injection to purge any MapLibre / OpenStreetMap attribution DOM elements in 1ms
  const purgeAttribution = () => {
    const targets = document.querySelectorAll(
      '.maplibregl-ctrl-attrib, details.maplibregl-ctrl-attrib, .maplibregl-compact, .maplibregl-compact-show'
    )
    targets.forEach(el => el.remove())
  }
  purgeAttribution()
  const attribObserver = new MutationObserver(purgeAttribution)
  if (mapContainer.value) {
    attribObserver.observe(mapContainer.value, { childList: true, subtree: true })
  }

  map.on('load', () => {
    purgeAttribution()
    updateMarkers()
    drawGeofenceCircle()
  })
}

const updateMarkers = () => {
  if (!map) return

  markers.forEach(m => m.remove())
  markers = []

  props.tasks.forEach(t => {
    const el = document.createElement('div')
    el.className = `custom-map-pin ${props.selectedTask?.id === t.id ? 'selected' : ''}`
    el.innerText = `${t.reward_sol.toFixed(2)} SOL`

    el.addEventListener('click', (e) => {
      e.stopPropagation()
      emit('selectTask', t)
    })

    const marker = new maplibregl.Marker({ element: el })
      .setLngLat([t.longitude, t.latitude])
      .addTo(map!)

    markers.push(marker)
  })
}

const drawGeofenceCircle = () => {
  if (!map || !map.isStyleLoaded()) return

  if (map.getLayer('geofence-fill')) map.removeLayer('geofence-fill')
  if (map.getLayer('geofence-line')) map.removeLayer('geofence-line')
  if (map.getSource('geofence')) map.removeSource('geofence')

  if (!props.selectedTask) return

  // Create 150m circle polygon GeoJSON
  const center = [props.selectedTask.longitude, props.selectedTask.latitude]
  const radiusInKm = 0.15
  const points = 64
  const coords: number[][] = []

  const distanceX = radiusInKm / (111.32 * Math.cos((center[1] * Math.PI) / 180))
  const distanceY = radiusInKm / 110.574

  for (let i = 0; i < points; i++) {
    const theta = (i / points) * (2 * Math.PI)
    const x = distanceX * Math.cos(theta)
    const y = distanceY * Math.sin(theta)
    coords.push([center[0] + x, center[1] + y])
  }
  coords.push(coords[0])

  map.addSource('geofence', {
    type: 'geojson',
    data: {
      type: 'Feature',
      geometry: {
        type: 'Polygon',
        coordinates: [coords]
      },
      properties: {}
    }
  })

  map.addLayer({
    id: 'geofence-fill',
    type: 'fill',
    source: 'geofence',
    paint: {
      'fill-color': '#FFD60A',
      'fill-opacity': 0.15
    }
  })

  map.addLayer({
    id: 'geofence-line',
    type: 'line',
    source: 'geofence',
    paint: {
      'line-color': '#1A1A17',
      'line-width': 1.5,
      'line-dasharray': [2, 2]
    }
  })

  // Smooth easeTo without bouncing or zooming out-and-in
  map.easeTo({
    center: [props.selectedTask.longitude, props.selectedTask.latitude],
    zoom: 14.5,
    duration: 600,
    essential: true
  })
}

watch(() => props.selectedTask, () => {
  updateMarkers()
  drawGeofenceCircle()
})

watch(() => props.tasks, (newTasks) => {
  updateMarkers()
  if (map && newTasks && newTasks.length > 0 && !props.selectedTask) {
    const avgLng = newTasks.reduce((acc, t) => acc + t.longitude, 0) / newTasks.length
    const avgLat = newTasks.reduce((acc, t) => acc + t.latitude, 0) / newTasks.length
    map.easeTo({
      center: [avgLng, avgLat],
      zoom: 12.5,
      duration: 600,
      essential: true
    })
  }
}, { deep: true })

onMounted(() => {
  initMap()
})

onUnmounted(() => {
  if (map) map.remove()
})
</script>

<template>
  <div class="w-full h-full relative">
    <div ref="mapContainer" class="w-full h-full"></div>
  </div>
</template>
