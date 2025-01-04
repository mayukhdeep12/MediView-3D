<script setup lang="ts">
import { storeToRefs } from 'pinia';
import { ref, computed, watch } from 'vue';
import { loadUserPromptedFiles } from '@/src/actions/loadUserFiles';
import useRemoteSaveStateStore from '@/src/store/remote-save-state';
import CloseableDialog from '@/src/components/CloseableDialog.vue';
import SaveSession from '@/src/components/SaveSession.vue';
import ControlButton from '@/src/components/ControlButton.vue';
import MessageNotifications from '@/src/components/MessageNotifications.vue';
import Settings from '@/src/components/Settings.vue';
import ControlsStripTools from '@/src/components/ControlsStripTools.vue';
import MessageCenter from '@/src/components/MessageCenter.vue';
import { MessageType, useMessageStore } from '@/src/store/messages';
import { ConnectionState, useServerStore } from '@/src/store/server';
import { useViewStore } from '@/src/store/views';
import { Layouts, DefaultLayoutName } from '@/src/config';

interface Props {
  hasData: boolean;
}

defineProps<Props>();

function useViewLayout() {
  const viewStore = useViewStore();
  const layoutName = ref(DefaultLayoutName);
  const { layout: currentLayout } = storeToRefs(viewStore);

  watch(
    layoutName,
    () => {
      const layout = Layouts[layoutName.value] || [];
      viewStore.setLayout(layout);
    },
    { immediate: true }
  );

  watch(currentLayout, () => {
    if (currentLayout.value?.name && currentLayout.value.name !== layoutName.value) {
      layoutName.value = currentLayout.value.name;
    }
  });

  return layoutName;
}

function useSaveControls() {
  const remoteSaveStateStore = useRemoteSaveStateStore();
  const { isSaving, saveUrl } = storeToRefs(remoteSaveStateStore);
  const saveDialog = ref(false);

  const handleSave = () => {
    if (saveUrl.value !== '') {
      remoteSaveStateStore.saveState();
    } else {
      saveDialog.value = true;
    }
  };

  return { handleSave, isSaving, saveDialog };
}

function useMessageBubble() {
  const messageStore = useMessageStore();
  const count = computed(() => messageStore.importantMessages.length);
  const badgeColor = computed(() => {
    if (messageStore.importantMessages.find((msg) => msg.type === MessageType.Error)) {
      return 'rgb(244, 67, 54)';
    }
    if (messageStore.importantMessages.find((msg) => msg.type === MessageType.Warning)) {
      return 'rgb(255, 167, 38)';
    }
    return 'rgb(33, 150, 243)';
  });

  return { count, badgeColor };
}

function useServerConnection() {
  const serverStore = useServerStore();
  const icon = computed(() => {
    switch (serverStore.connState) {
      case ConnectionState.Connected:
        return 'mdi-lan-check';
      case ConnectionState.Disconnected:
        return 'mdi-lan-disconnect';
      case ConnectionState.Pending:
        return 'mdi-lan-pending';
      default:
        throw new Error('Invalid connection state');
    }
  });

  const { url } = storeToRefs(serverStore);
  return { icon, url };
}

const settingsDialog = ref(false);
const messageDialog = ref(false);
const { icon: connIcon, url: serverUrl } = useServerConnection();
const layoutName = useViewLayout();
const { handleSave, saveDialog, isSaving } = useSaveControls();
const { count: msgCount, badgeColor: msgBadgeColor } = useMessageBubble();
</script>

<template>
  <aside class="tools-strip">
    <div class="tools-content">
      <!-- Top Tools Group -->
      <div class="tools-section">
        <control-button
          class="tool-button"
          icon="mdi-folder-open"
          @click="loadUserPromptedFiles"
        >
          <v-tooltip activator="parent" location="right" class="tooltip">
            <div class="tooltip-content">Open Files</div>
          </v-tooltip>
        </control-button>
        
        <control-button
          class="tool-button"
          :class="{ 'is-loading': isSaving }"
          icon="mdi-content-save-all"
          :loading="isSaving"
          @click="handleSave"
        >
          <v-tooltip activator="parent" location="right" class="tooltip">
            <div class="tooltip-content">Save Session</div>
          </v-tooltip>
        </control-button>
      </div>

      <!-- Middle Tools Group -->
      <div class="tools-section">
        <v-menu
          location="right"
          :close-on-content-click="true"
          transition="scale-transition"
        >
          <template v-slot:activator="{ props }">
            <control-button
              v-bind="props"
              class="tool-button"
              icon="mdi-view-dashboard"
            >
              <v-tooltip activator="parent" location="right" class="tooltip">
                <div class="tooltip-content">Layout Options</div>
              </v-tooltip>
            </control-button>
          </template>
          
          <v-card class="layout-menu">
            <v-card-text>
              <v-radio-group v-model="layoutName" density="compact">
                <v-radio
                  v-for="(value, key) in Layouts"
                  :key="key"
                  :label="value.name"
                  :value="key"
                  color="primary"
                  class="layout-radio"
                />
              </v-radio-group>
            </v-card-text>
          </v-card>
        </v-menu>

        <controls-strip-tools v-if="hasData" />
      </div>

      <!-- Bottom Tools Group -->
      <div class="tools-section">
        <control-button
          v-if="serverUrl"
          class="tool-button"
          :icon="connIcon"
        >
          <v-tooltip activator="parent" location="right" class="tooltip">
            <div class="tooltip-content">Server Status</div>
          </v-tooltip>
        </control-button>

        <div class="notification-container">
          <v-badge
            :content="msgCount.toString()"
            :color="msgBadgeColor"
            :model-value="msgCount > 0"
            location="top end"
            offset-x="3"
            offset-y="3"
            class="notification-badge"
          >
            <control-button
              class="tool-button"
              icon="mdi-bell-outline"
              @click="messageDialog = true"
            >
              <v-tooltip activator="parent" location="right" class="tooltip">
                <div class="tooltip-content">Notifications</div>
              </v-tooltip>
            </control-button>
          </v-badge>
        </div>

        <control-button
          class="tool-button"
          icon="mdi-cog"
          @click="settingsDialog = true"
        >
          <v-tooltip activator="parent" location="right" class="tooltip">
            <div class="tooltip-content">Settings</div>
          </v-tooltip>
        </control-button>
      </div>
    </div>
  </aside>

  <!-- Dialogs -->
  <closeable-dialog v-model="saveDialog" max-width="400px" class="modern-dialog">
    <template v-slot="{ close }">
      <save-session :close="close" />
    </template>
  </closeable-dialog>

  <closeable-dialog v-model="messageDialog" class="modern-dialog full-height">
    <message-center />
  </closeable-dialog>

  <message-notifications @open-notifications="messageDialog = true" />

  <closeable-dialog v-model="settingsDialog" class="modern-dialog">
    <settings />
  </closeable-dialog>
</template>

<style scoped>
.tools-strip {
  position: relative;
  width: 64px;
  background: #18181b;
  border-left: 1px solid rgba(255, 255, 255, 0.08);
  display: flex;
  flex-direction: column;
  align-items: center;
  box-shadow: -4px 0 20px rgba(0, 0, 0, 0.3);
  z-index: 10;
  height: 100%;
  overflow: hidden;
}

.tools-content {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 16px 0;
  overflow-y: auto;
  overflow-x: hidden;
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 255, 255, 0.2) transparent;
}

/* Webkit scrollbar styles */
.tools-content::-webkit-scrollbar {
  width: 4px;
}

.tools-content::-webkit-scrollbar-track {
  background: transparent;
}

.tools-content::-webkit-scrollbar-thumb {
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 4px;
}

.tools-content::-webkit-scrollbar-thumb:hover {
  background-color: rgba(255, 255, 255, 0.3);
}

.tools-section {
  display: flex;
  flex-direction: column;
  align-items: center; /* Center all items horizontally */
  gap: 12px;
  padding: 0;
  min-height: min-content;
  width: 100%;
}

/* Top section */
.tools-section:first-child {
  flex: 0 0 auto;
}

/* Middle section */
.tools-section:nth-child(2) {
  flex: 1 1 auto;
  min-height: auto;
}

/* Bottom section */
.tools-section:last-child {
  flex: 0 0 auto;
  margin-top: auto;
}

.tool-button {
  position: relative;
  width: 40px;
  height: 40px;
  min-height: 40px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.03);
  color: #9f9fa8;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid rgba(255, 255, 255, 0.06);
  cursor: pointer;
  flex-shrink: 0;
}

.notification-container {
  position: relative;
  width: 40px; /* Match tool-button width */
  display: flex;
  justify-content: center;
  align-items: center;
}

.layout-menu {
  background: #27272a;
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  overflow: hidden;
  min-width: 220px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
}

.layout-radio {
  padding: 10px 18px;
  margin: 4px 0;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.layout-radio:hover {
  background: rgba(255, 255, 255, 0.06);
}

:deep(.modern-dialog .v-card) {
  background: #27272a;
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.5);
}

.is-loading {
  position: relative;
  overflow: hidden;
}

.is-loading::after {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 200%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.15),
    transparent
  );
  animation: loading 1.8s cubic-bezier(0.4, 0, 0.2, 1) infinite;
}

@keyframes loading {
  from {
    transform: translateX(-100%);
  }
  to {
    transform: translateX(100%);
  }
}

:deep(.notification-badge .v-badge__badge) {
  font-size: 11px;
  min-width: 20px;
  min-height: 20px;
  border: 2px solid #18181b;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
}

:deep(.v-tooltip > .v-overlay__content) {
  background: #27272a;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
  padding: 4px 8px;
  font-size: 12px;
  color: #ffffff;
  white-space: nowrap;
}
</style>