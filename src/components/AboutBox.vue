<template>
  <v-card>
    <v-card-title class="d-flex flex-row justify-center text-h4">
      MediView 3D
    </v-card-title>
    <v-alert color="primary" variant="tonal" class="notice">
      Advanced Medical Image Analysis
    </v-alert>
    <v-card-text>
      <v-btn
        class="my-2"
        @click="openKeyboardShortcuts"
        prepend-icon="mdi-keyboard"
        color="primary"
      >
        Keyboard Shortcuts and View Controls
      </v-btn>
      <h2 class="mt-2">About MediView 3D</h2>
      <v-divider class="mb-2" />
      <p>
        MediView 3D is a state-of-the-art medical imaging platform designed for advanced radiological analysis 
        and diagnosis. Our platform combines cutting-edge AI technology with traditional radiological tools
        to provide comprehensive imaging solutions.
      </p>

      <ul>
        <li>
          Advanced AI Integration: Powered by deep learning algorithms for automated lesion detection and analysis
        </li>
        <li>
          Multi-modality Support: Seamless handling of CT, MRI, X-ray, and ultrasound imaging
        </li>
        <li>
          Real-time Processing: Instant image processing and analysis with cloud-optimized architecture
        </li>
        <li>
          Collaborative Platform: Built-in tools for medical professionals to share and discuss cases
        </li>
        <li>
          HIPAA Compliant: Enterprise-grade security with full regulatory compliance
        </li>
      </ul>
      <br />
      MediView 3D is built on robust open-source technologies and modern web frameworks, ensuring reliability
      and scalability. Our platform utilizes advanced image processing libraries and machine learning 
      models specifically optimized for medical imaging applications.
      <br />
      <br />
      Need specialized features or enterprise integration?
      <a
        rel="noopener noreferrer"
        target="_blank"
        href="#contact"
      >Contact our team</a>

      <h2 class="mt-2">Resources</h2>
      <v-divider class="mb-2" />
      <ul>
        <li>
          <span>Documentation: </span>
          <a
            rel="noopener noreferrer"
            target="_blank"
            href=""
          >
            Coming Soon
          </a>
        </li>
        <li>
          <span>Support Portal: </span>
          <a
            rel="noopener noreferrer"
            target="_blank"
            href=""
          >
            Coming Soon
          </a>
        </li>
        <li>
          <span>Training Resources: </span>
          <a
            rel="noopener noreferrer"
            target="_blank"
            href=""
          >
            Coming Soon
          </a>
        </li>
      </ul>
      <h2>System Information</h2>
      <v-divider class="mb-2" />
      <ul>
        <li>
          <div class="d-flex flex-flow align-center text-no-wrap">
            <span>MediView 3D Version: </span>
            <v-badge inline :content="versions.mediview" />
          </div>
        </li>
        <li>
          <div class="d-flex flex-flow align-center text-no-wrap">
            <span>AI Engine: </span>
            <v-badge inline :content="versions.aiEngine" />
          </div>
        </li>
        <li>
          <div class="d-flex flex-flow align-center text-no-wrap">
            <span>Image Processing Core: </span>
            <v-badge inline :content="versions.imageCore" />
          </div>
        </li>
      </ul>
      <h2 class="mt-2">Certifications</h2>
      <v-divider class="mb-2" />
      MediView 3D is FDA-cleared and CE-marked for clinical use in radiology departments and imaging centers.
      Our platform maintains compliance with international healthcare standards including HIPAA, GDPR, and ISO 13485.
      <br />
      <br />
      Research collaborations:
      <ul>
        <li>
          Stanford Medical Imaging Lab
        </li>
        <li>
          European Institute of Biomedical Imaging Research
        </li>
        <li>
          National Cancer Institute - Imaging Research Program
        </li>
      </ul>
    </v-card-text>
  </v-card>
</template>

<style scoped>
.notice {
  width: fit-content;
  margin: 0 auto;
  text-transform: uppercase;
  font-weight: 500;
  letter-spacing: 1px;
}

.v-card-title {
  background: linear-gradient(45deg, #2196F3, #1976D2);
  color: white;
  padding: 1.5rem;
}

.v-card {
  max-width: 1200px;
  margin: 0 auto;
}

h2 {
  color: #1976D2;
  margin-top: 1.5rem;
}
</style>

<script>
import { defineComponent } from 'vue';
import { useDisplay } from 'vuetify';
import { useKeyboardShortcutsStore } from '../store/keyboard-shortcuts';

export default defineComponent({
  name: 'AboutBox',
  setup() {
    const display = useDisplay();
    const keyboardStore = useKeyboardShortcutsStore();
    
    const openKeyboardShortcuts = () => {
      keyboardStore.settingsOpen = true;
    };

    return {
      openKeyboardShortcuts,
      mobile: display.xs,
      versions: {
        mediview: '2.1.0',
        aiEngine: '3.4.2',
        imageCore: '1.8.0',
      },
    };
  },
});
</script>