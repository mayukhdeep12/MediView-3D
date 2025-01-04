<template>
  <div
    class="slice-slider"
    ref="handleContainer"
    @pointerdown="onDragStart"
    @pointermove="onDragMove"
    @pointerup="onDragEnd"
    @pointercancel="onDragEnd"
    @contextmenu="$event.preventDefault()"
  >
    <div class="slice-slider-track"></div>
    <div
      class="slice-slider-handle"
      ref="handle"
      :style="{
        height: `${handleHeight}px`,
        transform: `translate3d(0, ${handlePosition}px, 0)`,
      }"
    >
        <div class="handle-inner"></div>
    </div>
  </div>
</template>

<script>
function getYOffsetFromTransform(matStr) {
  if (!matStr || matStr === 'none') {
    return 0;
  }
  const values = matStr
    .match(/matrix(?:3d)?\((.+)\)/)[1]
    .split(',')
    .map((v) => Number(v));
  const is3D = matStr.includes('3d');
  return is3D ? values[13] : values[5];
}

export default {
  props: {
    modelValue: {
      type: Number,
      default: 0,
    },
    min: {
      type: Number,
      required: true,
    },
    max: {
      type: Number,
      required: true,
    },
    step: {
      type: Number,
      required: true,
    },
    handleHeight: {
      type: Number,
      default: 20,
    },
    trackColor: {
      type: String,
      default: '#e0e0e0' // Light gray track
    },
    handleColor: {
      type: String,
      default: '#2196f3' // Blue handle
    },
    handleBorderColor: {
      type: String,
      default: '#1976d2'
    }
  },

  emits: ['update:modelValue'],

  data() {
    return {
      maxHandlePos: 0,
      dragging: false,
      initialHandlePos: 0,
      initialMousePosY: 0,
      yOffset: 0,
    };
  },

  computed: {
    handlePosition() {
      const range = this.max - this.min <= 0 ? 1 : this.max - this.min;
      const pos = this.maxHandlePos * ((this.modelValue - this.min) / range);
      return this.dragging ? this.draggingHandlePos : pos;
    },
    draggingHandlePos() {
      return Math.min(
        Math.max(0, this.initialHandlePos + this.yOffset),
        this.maxHandlePos
      );
    },
  },

  mounted() {
    this.updateMaxHandlePos();
    this.resizeObserver = new ResizeObserver((entries) => {
      if (entries.length === 1) {
        this.updateMaxHandlePos();
      }
    });
    this.resizeObserver.observe(this.$refs.handleContainer);
  },

  beforeUnmount() {
    this.resizeObserver.disconnect();
  },

  methods: {
    updateMaxHandlePos() {
      this.maxHandlePos =
        this.$refs.handleContainer.clientHeight - this.handleHeight;
    },

    onDragStart(ev) {
      ev.preventDefault();

      this.dragging = true;
      this.initialMousePosY = ev.pageY;

      if (ev.target === this.$refs.handle) {
        const handleStyles = window.getComputedStyle(this.$refs.handle);
        this.initialHandlePos = getYOffsetFromTransform(handleStyles.transform);
      } else {
        const { y } = this.$refs.handleContainer.getBoundingClientRect();
        this.initialHandlePos = Math.max(
          0,
          Math.min(this.maxHandlePos, ev.pageY - y - this.handleHeight / 2)
        );
        const newSlice = this.getNearestSlice(this.initialHandlePos);
        this.$emit('update:modelValue', newSlice);
      }

      this.yOffset = 0;

      this.$refs.handleContainer.setPointerCapture(ev.pointerId);
    },

    onDragMove(ev) {
      if (!this.$refs.handleContainer.hasPointerCapture(ev.pointerId)) return;
      ev.preventDefault();

      this.yOffset = ev.pageY - this.initialMousePosY;
      const slice = this.getNearestSlice(this.handlePosition);
      this.$emit('update:modelValue', slice);
    },

    onDragEnd(ev) {
      if (!this.$refs.handleContainer.hasPointerCapture(ev.pointerId)) return;
      ev.preventDefault();
      this.$refs.handleContainer.releasePointerCapture(ev.pointerId);

      this.dragging = false;
      const slice = this.getNearestSlice(this.handlePosition);
      this.$emit('update:modelValue', slice);
    },

    getNearestSlice(pos) {
      const sliceEstimate = pos / this.maxHandlePos;
      const frac = sliceEstimate * (this.max - this.min) + this.min;
      return Math.round(frac / this.step) * this.step;
    },
  },
};
</script>

<style scoped>
.slice-slider {
  touch-action: none;
  width: 20px; /* Adjust width as needed */
  padding: 10px 0; /* Add some vertical padding */
  display: inline-block; /* Prevent slider from taking full width */
}

.slice-slider-track {
  position: absolute;
  top: 10px;
  bottom: 10px;
  left: 50%;
  transform: translateX(-50%);
  width: 4px;
  border-radius: 2px;
  background-color: v-bind(trackColor);
}

.slice-slider-handle {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  width: 12px;
  border-radius: 50%;
  box-sizing: border-box;
  background-color: v-bind(handleColor);
  border: 2px solid v-bind(handleBorderColor);
  cursor: grab;
  transition: box-shadow 0.2s ease; /* Add transition for hover effect */
}

.slice-slider-handle:hover {
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
}

.slice-slider-handle:active{
    cursor: grabbing;
}
</style>