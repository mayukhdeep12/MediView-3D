<script setup lang="ts">
import {
  errorReportingConfigured,
  useErrorReporting,
} from '@/src/utils/errorReporting';
import { computed } from 'vue';

const errorStore = useErrorReporting();
const reportingEnabled = computed({
  get: () => !errorStore.disableReporting,
  set: (enabled) => {
    errorStore.disableReporting = !enabled;
  },
});
</script>

<template>
  <v-card class="text-grey-lighten-1">
    <v-card-title>Data Privacy and Security Notice</v-card-title>
    <v-card-text>
      <p class="mb-4">
        mediview-3d takes data privacy and security seriously. Here is how we keep
        your data safe.
      </p>
      <ul class="bullet-points">
        <li>
          <span class="font-weight-bold">Data Loading</span>: Your image data
          never leaves your computer. Images are loaded into your browser and
          are never sent to any remote server or cloud service.
        </li>
        <li>
          <span class="font-weight-bold">Error Reporting</span>: We collect
          error reports in the event that mediview-3d encounters issues. These
          reports help us improve mediview-3d's stability and only consist of code
          stack traces where applicable. We do not collect your data, nor any
          other identifiable information.
        </li>
      </ul>
      <p>
        If you would like to opt-out of error reporting, you may turn it off
        using the following setting. Your choice will be respected for future
        mediview-3d sessions on this machine.
      </p>
      <p class="mt-4 ml-4">
        <v-switch
          v-if="errorReportingConfigured"
          v-model="reportingEnabled"
          :label="`Error Reporting: ${reportingEnabled ? 'On' : 'Off'}`"
          color="secondary"
          hide-details
        />
        <v-alert v-else type="info" variant="text">
          <span>Error reporting has been turned off at build time.</span>
        </v-alert>
      </p>
    </v-card-text>
  </v-card>
</template>

<style scoped>
.bullet-points {
  padding-left: 20px;
  margin-bottom: 16px;
}

.bullet-points > li:not(:last-child) {
  margin-bottom: 8px;
}
</style>
