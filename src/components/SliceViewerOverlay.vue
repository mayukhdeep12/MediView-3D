<script setup lang="ts">
import { inject, toRefs } from 'vue';
import ViewOverlayGrid from '@/src/components/ViewOverlayGrid.vue';
import { useSliceConfig } from '@/src/composables/useSliceConfig';
import { Maybe } from '@/src/types';
import { VtkViewContext } from '@/src/components/vtk/context';
import { useWindowingConfig } from '@/src/composables/useWindowingConfig';
import { useOrientationLabels } from '@/src/composables/useOrientationLabels';
import DicomQuickInfoButton from '@/src/components/DicomQuickInfoButton.vue';

interface Props {
  viewId: string;
  imageId: Maybe<string>;
}

const props = defineProps<Props>();
const { viewId, imageId } = toRefs(props);

const view = inject(VtkViewContext);
if (!view) throw new Error('No VtkView');

const { top: topLabel, left: leftLabel } = useOrientationLabels(view);

const {
  config: sliceConfig,
  slice,
  range: sliceRange,
} = useSliceConfig(viewId, imageId);
const {
  config: wlConfig,
  width: windowWidth,
  level: windowLevel,
} = useWindowingConfig(viewId, imageId);
</script>

<template>
  <view-overlay-grid class="overlay-no-events view-annotations">
    <template v-slot:top-center>
      <div class="annotation-cell">
        <span>{{ topLabel }}</span>
      </div>
    </template>
    <template v-slot:middle-left>
      <div class="annotation-cell">
        <span>{{ leftLabel }}</span>
      </div>
    </template>
    <template v-slot:bottom-left>
      <div class="annotation-cell annotations-bottom-left">
        <div v-if="sliceConfig" class="annotation-item">
          <div class="annotation-label">Slice</div>
          <div class="annotation-value">{{ slice + 1 }}/{{ sliceRange[1] + 1 }}</div>
        </div>
        <div v-if="wlConfig" class="annotation-item">
          <div class="annotation-label">W/L</div>
          <div class="annotation-value">{{ windowWidth.toFixed(2) }} / {{ windowLevel.toFixed(2) }}</div>
        </div>
      </div>
    </template>
    <template v-slot:top-right>
      <div class="annotation-cell">
        <dicom-quick-info-button :image-id="imageId"></dicom-quick-info-button>
      </div>
    </template>
  </view-overlay-grid>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap'); /* Use Inter font */

.annotations-bottom-left {
  display: flex;
  flex-direction: column;
  gap: 6px; /* Increased spacing */
}

.annotation-item {
  display: grid;
  grid-template-columns: auto 1fr; /* Use grid for layout */
  align-items: center;
  padding: 6px 10px; /* Increased padding */
  border-radius: 8px; /* More rounded corners */
  background-color: rgba(30, 30, 30, 0.8); /* Darker background */
  color: #eee; /* Lighter text color */
  font-family: 'Inter', sans-serif;
  font-size: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Subtle shadow */
  backdrop-filter: blur(5px); /* Add a subtle blur */
  border: 1px solid rgba(255, 255, 255, 0.05); /* Very subtle border */
}

.annotation-label {
  font-weight: 600; /* Semi-bold */
  color: #ddd; /* Slightly lighter label color */
  margin-right: 8px;
}

/* Optional: Add a subtle hover effect */
.annotation-item:hover {
  background-color: rgba(40, 40, 40, 0.9);
}

/* Styles for other annotation cells (if needed) */
.annotation-cell {
    font-family: 'Inter', sans-serif;
    color: #eee;
}
</style>