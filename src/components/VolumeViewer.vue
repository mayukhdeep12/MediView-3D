<template>
  <div class="vtk-container-wrapper volume-viewer-container" tabindex="0">
    <div class="vtk-container" data-testid="two-view-container">
      <div class="vtk-sub-container">
        <vtk-volume-view
          class="vtk-view"
          ref="vtkView"
          data-testid="vtk-view vtk-two-view"
          :view-id="id"
          :image-id="currentImageID"
          :view-direction="viewDirection"
          :view-up="viewUp"
        >
          <vtk-base-volume-representation
            :view-id="id"
            :image-id="currentImageID"
          ></vtk-base-volume-representation>
          <vtk-orientation-marker></vtk-orientation-marker>
          <crop-tool :view-id="viewId" :image-id="currentImageID"></crop-tool>
          <slot></slot>
        </vtk-volume-view>
      </div>
      <view-overlay-grid class="overlay-no-events view-annotations">
        <template v-slot:top-left>
          <div class="annotation-cell">
            <div class="controls-wrapper">
              <v-btn
                class="pointer-events-all camera-reset-btn"
                dark
                icon
                size="medium"
                variant="text"
                @click="resetCamera"
              >
                <RotateCcw class="h-5 w-5" />
                <v-tooltip
                  location="right"
                  activator="parent"
                  transition="slide-x-transition"
                >
                  Reset Camera
                </v-tooltip>
              </v-btn>
              <span class="preset-name">{{ presetName }}</span>
            </div>
          </div>
        </template>
      </view-overlay-grid>

      <transition name="loading">
        <div v-if="isImageLoading" class="overlay-no-events loading">
          <div class="loading-text">Loading the image</div>
          <div>
            <v-progress-circular indeterminate color="primary" />
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, toRefs, computed } from 'vue';
import { RotateCcw } from 'lucide-vue-next';
import { useCurrentImage } from '@/src/composables/useCurrentImage';
import { LPSAxisDir } from '@/src/types/lps';
import VtkVolumeView from '@/src/components/vtk/VtkVolumeView.vue';
import { VtkViewApi } from '@/src/types/vtk-types';
import { LayoutViewProps } from '@/src/types';
import VtkBaseVolumeRepresentation from '@/src/components/vtk/VtkBaseVolumeRepresentation.vue';
import { useViewAnimationListener } from '@/src/composables/useViewAnimationListener';
import CropTool from '@/src/components/tools/crop/CropTool.vue';
import { useWebGLWatchdog } from '@/src/composables/useWebGLWatchdog';
import VtkOrientationMarker from '@/src/components/vtk/VtkOrientationMarker.vue';
import ViewOverlayGrid from '@/src/components/ViewOverlayGrid.vue';
import useVolumeColoringStore from '@/src/store/view-configs/volume-coloring';
import { useResetViewsEvents } from '@/src/components/tools/ResetViews.vue';
import { whenever } from '@vueuse/core';

interface Props extends LayoutViewProps {
  viewDirection: LPSAxisDir;
  viewUp: LPSAxisDir;
}

const vtkView = ref<VtkViewApi>();

const props = defineProps<Props>();

const { id: viewId, type: viewType, viewDirection, viewUp } = toRefs(props);

function resetCamera() {
  if (!vtkView.value) return;
  vtkView.value.resetCamera();
  vtkView.value.renderer.updateLightsGeometryToFollowCamera();
}

useResetViewsEvents().onClick(resetCamera);

useWebGLWatchdog(vtkView);
useViewAnimationListener(vtkView, viewId, viewType);

const { currentImageID, isImageLoading } = useCurrentImage();

whenever(
  computed(() => !isImageLoading.value),
  () => {
    resetCamera();
  }
);

const coloringStore = useVolumeColoringStore();
const coloringConfig = computed(() =>
  coloringStore.getConfig(viewId.value, currentImageID.value)
);
const presetName = computed(
  () => coloringConfig.value?.transferFunction.preset.replace(/-/g, ' ') ?? ''
);
</script>

<style scoped>
@import '@/src/components/styles/vtk-view.css';
@import '@/src/components/styles/utils.css';

.volume-viewer-container {
  background-color: rgb(17, 24, 39);
  grid-template-columns: auto;
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
}

.controls-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 4px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(4px);
  border-radius: 8px;
}

.camera-reset-btn {
  background: transparent;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 8px;
  margin: -4px 0;
}

.camera-reset-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: scale(1.05);
}

.preset-name {
  font-size: 0.875rem;
  font-weight: 500;
  letter-spacing: 0.025em;
  color: rgba(255, 255, 255, 0.9);
  padding-right: 8px;
}

.loading-text {
  font-size: 1rem;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 1rem;
}

.loading {
  background: rgba(17, 24, 39, 0.8);
  backdrop-filter: blur(8px);
}
</style>