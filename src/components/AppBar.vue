<script setup>
import { ref } from 'vue';
import { useDisplay } from 'vuetify';
import CloseableDialog from '@/src/components/CloseableDialog.vue';
import AboutBox from '@/src/components/AboutBox.vue';

const emit = defineEmits(['click:left-menu']);

const { mobile } = useDisplay();
const aboutBoxDialog = ref(false);
</script>

<template>
  <v-app-bar 
    app 
    clipped-left 
    :height="56" 
    class="app-bar-modern"
    :elevation="1"
    :color="'surface'"
  >
    <v-btn 
      icon="mdi-menu" 
      @click="emit('click:left-menu')"
      class="menu-button"
      variant="text"
      :ripple="false"
    >
      <v-icon size="24">mdi-menu</v-icon>
    </v-btn>

    <v-toolbar-title class="d-flex flex-row align-center">
      <div class="title-container">
        <span class="app-title">MediView 3D</span>
        <span class="app-subtitle" v-if="!mobile">Dashboard</span>
      </div>
    </v-toolbar-title>

    <v-spacer></v-spacer>

    <div class="actions-container">
      <v-btn
        variant="text"
        icon
        class="action-button"
        @click="aboutBoxDialog = !aboutBoxDialog"
        :ripple="false"
      >
        <v-icon icon="mdi-information-outline"></v-icon>
        <v-tooltip 
          activator="parent" 
          location="bottom"
          transition="fade-transition"
        >
          About
        </v-tooltip>
      </v-btn>
    </div>
  </v-app-bar>

  <closeable-dialog v-model="aboutBoxDialog">
    <about-box />
  </closeable-dialog>
</template>

<style scoped>
.app-bar-modern {
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(var(--v-border-color), 0.12);
}

.menu-button {
  margin-right: 8px;
  transition: transform 0.2s ease;
}

.menu-button:hover {
  transform: scale(1.05);
}

.title-container {
  display: flex;
  flex-direction: column;
  line-height: 1.2;
}

.app-title {
  font-size: 1.25rem;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.app-subtitle {
  font-size: 0.75rem;
  opacity: 0.7;
  font-weight: 400;
}

.actions-container {
  display: flex;
  gap: 8px;
  align-items: center;
  margin-right: 8px;
}

.action-button {
  position: relative;
  width: 40px;
  height: 40px;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.action-button:hover {
  background-color: rgba(var(--v-theme-primary), 0.08);
}

.action-button .v-icon {
  transition: transform 0.2s ease;
}

.action-button:hover .v-icon {
  transform: scale(1.1);
}

/* Fade transition for tooltip */
.fade-transition-enter-active,
.fade-transition-leave-active {
  transition: opacity 0.2s ease;
}

.fade-transition-enter-from,
.fade-transition-leave-to {
  opacity: 0;
}
</style>