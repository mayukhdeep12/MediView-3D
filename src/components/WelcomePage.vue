<script setup lang="ts">
import { ref, computed } from 'vue';
import CloseableDialog from '@/src/components/CloseableDialog.vue';
import DataSecurityBox from '@/src/components/DataSecurityBox.vue';
import useRemoteSaveStateStore from '@/src/store/remote-save-state';

withDefaults(
  defineProps<{
    loading?: boolean;
  }>(),
  {
    loading: false,
  }
);

const isRemoteSaveDisabled = computed(
  () => useRemoteSaveStateStore().saveUrl === ''
);
const dataSecurityDialog = ref(false);
</script>

<template>
  <v-container class="page-container bg-gradient-to-br from-grey-darken-4 to-grey-darken-3" v-bind="$attrs">
    <v-col>
      <v-row justify="center">
        <v-card
          flat
          dark
          :class="['upload-card', { 'upload-card--loading': loading }]"
          color="grey-darken-3"
          class="text-center headline pa-10 rounded-lg"
          elevation="10"
        >
          <template v-if="!loading">
            <div class="upload-section">
              <div class="mb-8">
                <h2 class="text-h4 font-weight-medium mb-2">Upload Files</h2>
                <p class="text-grey-lighten-1">Import your DICOM files</p>
              </div>

              <div class="upload-area pa-8">
                <div class="icon-container mb-4">
                  <v-icon size="64" color="primary">mdi-folder-open</v-icon>
                </div>
                <div class="text-h6 mb-8">Click to open local files</div>

                <div class="divider">
                  <span class="divider-text">or</span>
                </div>

                <div class="icon-container mt-8">
                  <v-icon size="64" color="primary">mdi-arrow-down-bold</v-icon>
                </div>
                <div class="text-h6">Drag & drop your DICOM files</div>
              </div>
            </div>
          </template>

          <template v-else>
            <div class="loading-section">
              <div class="text-h5 mb-6">Loading data...</div>
              <v-progress-linear
                indeterminate
                color="primary"
                height="6"
                rounded
                class="loading-progress"
              />
            </div>
          </template>
        </v-card>
      </v-row>
    </v-col>
  </v-container>
  
  <closeable-dialog v-model="dataSecurityDialog">
    <data-security-box />
  </closeable-dialog>
</template>

<style scoped>
.page-container {
  flex: 1 1 auto;
  display: flex;
  flex-flow: row;
  align-items: center;
  max-width: 100%;
  min-height: 100vh;
}

.upload-card {
  max-width: 600px;
  width: 100%;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.upload-card:hover {
  border-color: var(--v-primary-base);
  transform: translateY(-2px);
}

.upload-area {
  border: 2px dashed rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  transition: all 0.3s ease;
}

.upload-area:hover {
  border-color: var(--v-primary-base);
  background: rgba(255, 255, 255, 0.05);
}

.icon-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100px;
}

.divider {
  display: flex;
  align-items: center;
  text-align: center;
  margin: 24px 0;
}

.divider::before,
.divider::after {
  content: '';
  flex: 1;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.divider-text {
  padding: 0 16px;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
}

.loading-section {
  padding: 32px;
}

.loading-progress {
  box-shadow: 0 0 10px rgba(var(--v-primary-base), 0.2);
}

.upload-card--loading {
  opacity: 0.8;
}

.vertical-offset-margin {
  margin-top: 128px;
}
</style>