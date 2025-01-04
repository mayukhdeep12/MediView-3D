<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { isRegularImage } from '@/src/utils/dataSelection';
import SampleDataBrowser from './SampleDataBrowser.vue';
import { useDicomWebStore } from '../store/dicom-web/dicom-web-store';
import ImageDataBrowser from './ImageDataBrowser.vue';
import PatientBrowser from './PatientBrowser.vue';
import PatientList from './dicom-web/PatientList.vue';
import { useDICOMStore } from '../store/datasets-dicom';
import { useImageStore } from '../store/datasets-images';
import { useDataBrowserStore } from '../store/data-browser';
import { useDatasetStore } from '../store/datasets';
import { removeFromArray } from '../utils';

const SAMPLE_DATA_KEY = 'sampleData';
const ANONYMOUS_DATA_KEY = 'anonymousData';
const DICOM_WEB_KEY = 'dicomWeb';

const dicomStore = useDICOMStore();
const imageStore = useImageStore();
const dicomWeb = useDicomWebStore();
const dataBrowserStore = useDataBrowserStore();
const datasetStore = useDatasetStore();

const patients = computed(() =>
  Object.entries(dicomStore.patientInfo)
    .map(([key, info]) => ({
      key,
      name: info.PatientName,
      info,
    }))
    .sort((a, b) => (a.name < b.name ? -1 : 1))
);

const hasAnonymousImages = computed(
  () => imageStore.idList.filter((id) => isRegularImage(id)).length > 0
);

const panels = ref<string[]>([SAMPLE_DATA_KEY, DICOM_WEB_KEY]);

watch(
  [hasAnonymousImages, patients] as const,
  ([showAnonymous, patients_]) => {
    const showPatients = patients_.length > 0;
    if (showAnonymous) {
      panels.value.push(ANONYMOUS_DATA_KEY);
    }
    if (showPatients) {
      panels.value.push(...patients_.map((patient) => patient.key));
    }
    if (showAnonymous || showPatients) {
      removeFromArray(panels.value, SAMPLE_DATA_KEY);
    }
  }
);

const hideSampleData = computed(() => dataBrowserStore.hideSampleData);

const deletePatient = (key: string) => {
  dicomStore.patientStudies[key]
    .flatMap((study) => dicomStore.studyVolumes[study])
    .forEach(datasetStore.remove);
};
</script>

<template>
  <div class="data-module">
    <div class="data-panels">
      <v-expansion-panels
        v-model="panels"
        multiple
        variant="accordion"
        class="panels-container"
      >
        <!-- Anonymous Images Panel -->
        <v-expansion-panel
          v-if="hasAnonymousImages"
          :value="ANONYMOUS_DATA_KEY"
          class="panel-item"
        >
          <v-expansion-panel-title class="panel-title-wrapper">
            <div class="panel-header">
              <div class="header-content">
                <div class="icon-container">
                  <div class="icon-wrapper">
                    <v-icon>mdi-image</v-icon>
                  </div>
                  <div class="icon-backdrop"></div>
                </div>
                <span class="title-text">Anonymous</span>
              </div>
            </div>
          </v-expansion-panel-title>
          <v-expansion-panel-text>
            <image-data-browser />
          </v-expansion-panel-text>
        </v-expansion-panel>

        <!-- Patient Panels -->
        <v-expansion-panel
          v-for="patient in patients"
          :key="patient.key"
          :value="patient.key"
          class="panel-item"
        >
          <v-expansion-panel-title class="panel-title-wrapper">
            <div class="patient-header">
              <div class="header-content">
                <div class="icon-container">
                  <div class="icon-wrapper">
                    <v-icon>mdi-account</v-icon>
                  </div>
                  <div class="icon-backdrop"></div>
                </div>
                <span class="title-text" :title="patient.name">
                  {{ patient.name }}
                </span>
              </div>
              <v-menu offset-x :close-on-content-click="true">
                <template v-slot:activator="{ props }">
                  <v-btn
                    v-bind="props"
                    variant="text"
                    icon="mdi-dots-vertical"
                    size="small"
                    class="action-button"
                    @click.stop
                  />
                </template>
                <v-list class="context-menu">
                  <v-list-item @click.stop="deletePatient(patient.key)" class="delete-item">
                    <template v-slot:prepend>
                      <v-icon size="small">mdi-delete</v-icon>
                    </template>
                    <v-list-item-title>Delete Patient</v-list-item-title>
                  </v-list-item>
                </v-list>
              </v-menu>
            </div>
          </v-expansion-panel-title>
          <v-expansion-panel-text>
            <patient-browser :patient-key="patient.key" />
          </v-expansion-panel-text>
        </v-expansion-panel>

        <!-- DICOM Web Panel -->
        <v-expansion-panel 
          v-if="dicomWeb.isConfigured" 
          :value="DICOM_WEB_KEY"
          class="panel-item"
        >
          <v-expansion-panel-title class="panel-title-wrapper">
            <div class="panel-header">
              <div class="header-content">
                <div class="icon-container">
                  <div class="icon-wrapper">
                    <v-icon>mdi-cloud-download</v-icon>
                  </div>
                  <div class="icon-backdrop"></div>
                </div>
                <span class="title-text">
                  {{ `${dicomWeb.hostName || dicomWeb.host} | DICOMWeb` }}
                </span>
              </div>
            </div>
          </v-expansion-panel-title>
          <v-expansion-panel-text>
            <patient-list />
          </v-expansion-panel-text>
        </v-expansion-panel>

        <!-- Sample Data Panel -->
        <v-expansion-panel 
          v-if="!hideSampleData" 
          :value="SAMPLE_DATA_KEY"
          class="panel-item"
        >
          <v-expansion-panel-title class="panel-title-wrapper">
            <div class="panel-header">
              <div class="header-content">
                <div class="icon-container">
                  <div class="icon-wrapper">
                    <v-icon>mdi-card-bulleted</v-icon>
                  </div>
                  <div class="icon-backdrop"></div>
                </div>
                <span class="title-text">Sample Data</span>
              </div>
            </div>
          </v-expansion-panel-title>
          <v-expansion-panel-text>
            <sample-data-browser />
          </v-expansion-panel-text>
        </v-expansion-panel>
      </v-expansion-panels>
      
      <div class="empty-state">
        <div class="empty-icon-wrapper">
          <v-icon size="32">mdi-database-off</v-icon>
        </div>
        <span>No data loaded</span>
        <div class="empty-subtitle">Import data to get started</div>
      </div>
    </div>
  </div>
</template>


<style scoped>
/* Core Layout */
.data-module {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: rgb(var(--v-theme-background));
  border-radius: 32px;
  margin: 24px;
  padding: 24px;
  position: relative;
  overflow: hidden;
  box-shadow: 
    0 24px 48px -12px rgba(0, 0, 0, 0.12),
    0 12px 24px -4px rgba(0, 0, 0, 0.08);
}

/* Background Effects */
.data-module::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 200px;
  background: linear-gradient(
    135deg,
    rgba(var(--v-theme-primary), 0.05),
    rgba(var(--v-theme-secondary), 0.05)
  );
  filter: blur(60px);
  z-index: 0;
}

/* Panel Container */
.data-panels {
  flex: 1;
  overflow-y: auto;
  border-radius: 24px;
  padding: 4px;
  position: relative;
  z-index: 1;
}

.panels-container {
  background: transparent !important;
  gap: 16px;
}

/* Panel Items */
.panel-item {
  border-radius: 24px !important;
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-theme-outline), 0.08);
  transition: all 0.4s cubic-bezier(0.2, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(20px);
}

.panel-item:hover {
  transform: translateY(-4px);
  border-color: rgba(var(--v-theme-primary), 0.2);
  box-shadow: 
    0 20px 40px rgba(0, 0, 0, 0.1),
    0 8px 16px rgba(0, 0, 0, 0.05);
}

/* Panel Headers */
.panel-title-wrapper {
  padding: 24px 16px !important;
  min-height: unset !important;
}

.panel-header,
.patient-header {
  display: flex;
  align-items: center;
  width: 100%;
  position: relative;
  padding: 0 8px;
}

/* Header Content */
.header-content {
  display: flex;
  align-items: center;
  gap: 20px;
  flex: 1;
  padding-right: 12px;
}

/* Icon Container */
.icon-container {
  position: relative;
  width: 48px;
  height: 48px;
  flex-shrink: 0;
  margin-right: 16px;
}

.icon-wrapper {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 16px;
  background: rgb(var(--v-theme-primary));
  color: white;
  transition: all 0.4s cubic-bezier(0.2, 0, 0.2, 1);
  z-index: 2;
}

.icon-backdrop {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100%;
  height: 100%;
  background: rgb(var(--v-theme-primary));
  filter: blur(12px);
  opacity: 0.3;
  transform: translate(-50%, -50%);
  transition: all 0.4s cubic-bezier(0.2, 0, 0.2, 1);
  z-index: 1;
  animation: glowPulse 3s ease-in-out infinite;
}

/* Typography */
.title-text {
  font-size: 1.1rem;
  font-weight: 600;
  color: rgb(var(--v-theme-on-surface));
  letter-spacing: 0.3px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  transition: all 0.3s ease;
  flex: 1;
  margin-left: 16px;
}

/* Action Buttons */
.action-button {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: rgba(var(--v-theme-surface-variant), 0.8);
  color: rgb(var(--v-theme-on-surface-variant));
  transition: all 0.3s cubic-bezier(0.2, 0, 0.2, 1);
  margin-left: auto;
  margin-right: 8px;
}

.action-button:hover {
  background: rgb(var(--v-theme-primary)) !important;
  color: white;
  transform: rotate(90deg);
}

/* Context Menu */
.context-menu {
  border-radius: 16px;
  background: rgb(var(--v-theme-surface));
  box-shadow: 
    0 12px 36px rgba(0, 0, 0, 0.2),
    0 6px 16px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  border: 1px solid rgba(var(--v-theme-outline), 0.08);
  padding: 8px;
}

.delete-item {
  border-radius: 12px;
  margin: 2px;
  transition: all 0.3s ease;
}

.delete-item:hover {
  background: rgba(var(--v-theme-error), 0.1) !important;
  color: rgb(var(--v-theme-error));
}

/* Empty State */
.empty-state {
  display: none;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 64px 32px;
  text-align: center;
  border-radius: 24px;
  margin: 24px 0;
  background: rgb(var(--v-theme-surface));
  border: 1px solid rgba(var(--v-theme-outline), 0.08);
}

.empty-icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 64px;
  height: 64px;
  border-radius: 20px;
  background: rgba(var(--v-theme-on-surface), 0.05);
  color: rgb(var(--v-theme-on-surface-variant));
  margin-bottom: 8px;
}

.empty-subtitle {
  font-size: 0.9rem;
  color: rgb(var(--v-theme-on-surface-variant));
  opacity: 0.7;
}

.panels-container:empty + .empty-state {
  display: flex;
}

/* Scrollbar Styling */
.data-panels::-webkit-scrollbar {
  width: 8px;
}

.data-panels::-webkit-scrollbar-track {
  background: transparent;
}

.data-panels::-webkit-scrollbar-thumb {
  background: rgba(var(--v-theme-on-surface), 0.1);
  border-radius: 4px;
  transition: all 0.3s ease;
}

.data-panels::-webkit-scrollbar-thumb:hover {
  background: rgba(var(--v-theme-primary), 0.3);
}

/* Panel Content */
:deep(.v-expansion-panel-text__wrapper) {
  padding: 28px !important;
  background: rgb(var(--v-theme-background));
  border-top: 1px solid rgba(var(--v-theme-outline), 0.08);
}

:deep(.v-expansion-panel-title__overlay) {
  display: none;
}

/* Animations */
@keyframes slideUp {
  from { 
    opacity: 0; 
    transform: translateY(20px);
  }
  to { 
    opacity: 1; 
    transform: translateY(0);
  }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes glowPulse {
  0% {
    filter: blur(12px);
    opacity: 0.3;
  }
  50% {
    filter: blur(16px);
    opacity: 0.4;
  }
  100% {
    filter: blur(12px);
    opacity: 0.3;
  }
}

/* Animation Applications */
.panel-item {
  animation: slideUp 0.5s cubic-bezier(0.2, 0, 0.2, 1);
  animation-fill-mode: both;
}

.panel-item:nth-child(2) { animation-delay: 0.1s; }
.panel-item:nth-child(3) { animation-delay: 0.2s; }
.panel-item:nth-child(4) { animation-delay: 0.3s; }

/* Hover Effects */
.panel-item:hover .icon-wrapper {
  transform: scale(1.1) translateY(-2px);
  background: linear-gradient(135deg, 
    rgb(var(--v-theme-primary)), 
    rgb(var(--v-theme-secondary))
  );
}

.panel-item:hover .icon-backdrop {
  width: 120%;
  height: 120%;
  opacity: 0.4;
}

/* Glass Morphism */
.panel-item::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.1),
    rgba(255, 255, 255, 0.05)
  );
  border-radius: 24px;
  pointer-events: none;
}

/* Responsive Design */
@media (max-width: 768px) {
  .data-module {
    margin: 16px;
    padding: 16px;
    border-radius: 24px;
  }

  .panel-title-wrapper {
    padding: 20px 12px !important;
  }

  .icon-container {
    width: 40px;
    height: 40px;
    margin-right: 12px;
  }

  .title-text {
    margin-left: 12px;
    font-size: 1rem;
  }

  .header-content {
    gap: 16px;
  }
}

@media (max-width: 480px) {
  .data-module {
    margin: 12px;
    padding: 12px;
    border-radius: 20px;
  }

  .panel-title-wrapper {
    padding: 16px 8px !important;
  }

  .header-content {
    gap: 12px;
  }

  .icon-container {
    margin-right: 8px;
  }

  .title-text {
    margin-left: 8px;
  }

  .empty-state {
    padding: 40px 20px;
  }
}

/* Accessibility */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}

/* Dark Mode Optimizations */
@media (prefers-color-scheme: dark) {
  .panel-item {
    background: rgba(var(--v-theme-surface), 0.8) !important;
  }

  .empty-state {
    background: rgba(var(--v-theme-surface), 0.8);
  }
}

/* High Contrast Mode */
@media (forced-colors: active) {
  .panel-item {
    border: 2px solid CanvasText;
  }

  .icon-wrapper {
    border: 1px solid CanvasText;
  }
}
</style>