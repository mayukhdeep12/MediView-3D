<template>
  <div class="module-root">
    <div class="module-switcher">
      <v-tabs
        id="module-switcher-tabs"
        v-model="selectedModuleIndex"
        icons-and-text
        show-arrows
        class="switcher-tabs"
      >
        <v-tab
          v-for="item in Modules"
          :key="item.name"
          :data-testid="`module-tab-${item.name}`"
          class="module-tab"
        >
          <div class="tab-content">
            <span class="module-name">{{ item.name }}</span>
            <v-icon class="tab-icon">mdi-{{ item.icon }}</v-icon>
          </div>
        </v-tab>
      </v-tabs>
    </div>
    <div class="module-container">
      <v-window v-model="selectedModuleIndex" touchless class="fill-height">
        <v-window-item
          v-for="mod in Modules"
          :key="mod.name"
          class="fill-height"
        >
          <component
            :key="mod.name"
            v-show="Modules[selectedModuleIndex] === mod"
            :is="mod.component"
          />
        </v-window-item>
      </v-window>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, defineComponent, ref, watch } from 'vue';

import DataBrowser from './DataBrowser.vue';
import RenderingModule from './RenderingModule.vue';
import AnnotationsModule from './AnnotationsModule.vue';
import { useToolStore } from '../store/tools';
import { Tools } from '../store/tools/types';

interface Module {
  name: string;
  icon: string;
  component: Component;
}

const Modules: Module[] = [
  {
    name: 'Data',
    icon: 'database',
    component: DataBrowser,
  },
  {
    name: 'Annotations',
    icon: 'pencil',
    component: AnnotationsModule,
  },
  {
    name: 'Rendering',
    icon: 'cube',
    component: RenderingModule,
  },
];

const autoSwitchToAnnotationsTools = [
  Tools.Rectangle,
  Tools.Ruler,
  Tools.Polygon,
  Tools.Paint,
];

export default defineComponent({
  name: 'ModulePanel',
  setup() {
    const selectedModuleIndex = ref(0);

    const toolStore = useToolStore();
    watch(
      () => toolStore.currentTool,
      (newTool) => {
        if (autoSwitchToAnnotationsTools.includes(newTool))
          selectedModuleIndex.value = 1;
      }
    );

    return {
      selectedModuleIndex,
      Modules,
    };
  },
});
</script>

<style scoped>
.module-root {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: var(--v-theme-surface);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.module-switcher {
  position: relative;
  background: var(--v-theme-surface-variant);
  padding: 0.5rem 1rem;
  border-bottom: 1px solid rgba(var(--v-theme-on-surface-variant), 0.1);
}

.switcher-tabs {
  background: transparent !important;
}

.module-tab {
  transition: all 0.3s ease;
  border-radius: 8px;
  margin: 0 4px;
  opacity: 0.7;
}

.module-tab:hover {
  opacity: 1;
  background: rgba(var(--v-theme-on-surface-variant), 0.05);
}

.module-tab.v-tab--selected {
  opacity: 1;
  background: rgba(var(--v-theme-primary), 0.1);
}

.tab-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 8px 16px;
  gap: 4px;
}

.module-name {
  font-size: 0.75rem;
  font-weight: 500;
  letter-spacing: 0.5px;
  color: rgb(var(--v-theme-on-surface));
}

.tab-icon {
  font-size: 1.25rem;
  color: rgb(var(--v-theme-primary));
}

.module-container {
  flex: 1;
  overflow: auto;
  padding: 1rem;
  background: var(--v-theme-surface);
}

#module-switcher-tabs :deep(.v-slide-group__content) {
  justify-content: center;
}

#module-switcher-tabs :deep(.v-slide-group__prev.v-slide-group__prev--disabled),
#module-switcher-tabs :deep(.v-slide-group__next.v-slide-group__next--disabled) {
  display: none;
}

/* Smooth scrollbar styling */
.module-container::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.module-container::-webkit-scrollbar-track {
  background: transparent;
}

.module-container::-webkit-scrollbar-thumb {
  background: rgba(var(--v-theme-on-surface-variant), 0.2);
  border-radius: 4px;
}

.module-container::-webkit-scrollbar-thumb:hover {
  background: rgba(var(--v-theme-on-surface-variant), 0.3);
}
</style>