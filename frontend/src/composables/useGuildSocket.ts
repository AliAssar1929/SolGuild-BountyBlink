import { ref, onMounted, onUnmounted } from 'vue'

export type GuildEvent = {
  event: 'QUEST_CREATED' | 'QUEST_CLAIMED' | 'SUBMISSION_VERIFIED' | 'QUEST_APPROVED' | 'QUEST_REFUNDED'
  task_id?: string
  title?: string
  reward_sol?: number
  city?: string
  category?: string
  status?: string
  worker_address?: string
  payout_tx_sig?: string
  passed?: boolean
}

export function useGuildSocket(onEventCallback?: (evt: GuildEvent) => void) {
  const isConnected = ref(false)
  let socket: WebSocket | null = null
  let reconnectTimer: any = null

  const connect = () => {
    try {
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
      const wsUrl = `${protocol}//${window.location.host}/ws/quests`
      socket = new WebSocket(wsUrl)

      socket.onopen = () => {
        isConnected.value = true
        console.log('⚡ [SolGuild] Realtime WebSocket connected')
      }

      socket.onmessage = (event) => {
        try {
          const data: GuildEvent = JSON.parse(event.data)
          if (onEventCallback) {
            onEventCallback(data)
          }
        } catch (e) {
          console.warn('Socket message parse error:', e)
        }
      }

      socket.onclose = () => {
        isConnected.value = false
        // Reconnect after 3 seconds
        clearTimeout(reconnectTimer)
        reconnectTimer = setTimeout(connect, 3000)
      }

      socket.onerror = () => {
        socket?.close()
      }
    } catch (e) {
      console.warn('WebSocket init exception:', e)
      clearTimeout(reconnectTimer)
      reconnectTimer = setTimeout(connect, 4000)
    }
  }

  onMounted(() => {
    connect()
  })

  onUnmounted(() => {
    clearTimeout(reconnectTimer)
    if (socket) {
      socket.close()
    }
  })

  return {
    isConnected
  }
}
