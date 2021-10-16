<template>
  <div
    ref="card"
    :class="{ 'swipe-card': true, animate: shouldAnimate, 'shadow-sm': true }"
    :style="{ transform: `translate(${position.x}px, ${position.y}px) rotate(${rotation}deg)` }"
  >
    <div class="card position-relative">
      <img :src="productImageURL" class="card-img-top" :alt="product.name" />
      <div class="card-body">
        <div class="card-text text-left">
          <div class="product-name mb-1">{{ product.name }}</div>

          <p class="mb-0">{{ product.description }}</p>
        </div>
      </div>

      <div class="right-overlay" :style="{ '--ratio': swipeRightRatio }"><i class="far fa-check-circle"></i></div>
      <div class="left-overlay" :style="{ '--ratio': swipeLeftRatio }"><i class="far fa-times-circle"></i></div>
    </div>
  </div>
</template>

<script>
import interact from 'interactjs';
import { getProductImageUrl } from '@/util/getProductImageUrl';
import { clamp } from '@/util/clamp';
import { formatPrice } from '@/util/formatPrice';

const SWIPE_THRESHOLD = window.innerWidth / 3;
const MAX_ROTATION_DEGREES = 20;

const DEFAULT_POSITION = {
  x: 0,
  y: 0,
};

export default {
  name: 'SwipeCard',
  props: {
    product: { type: Object, required: true },
  },
  data: () => {
    return {
      position: DEFAULT_POSITION,
      shouldAnimate: false,
    };
  },
  computed: {
    productImageURL() {
      return getProductImageUrl(this.product);
    },
    formattedPrice() {
      return formatPrice(this.product.price);
    },
    cardElement() {
      return this.$refs.card;
    },
    swipeRatio() {
      return clamp(this.position.x / SWIPE_THRESHOLD, -1, 1);
    },
    rotation() {
      return this.swipeRatio * MAX_ROTATION_DEGREES;
    },
    swipeRightRatio() {
      return Math.max(0, this.swipeRatio);
    },
    swipeLeftRatio() {
      return Math.abs(Math.min(this.swipeRatio, 0));
    },
  },
  methods: {
    getNewPosition(event) {
      const x = this.position.x + event.dx;
      const y = this.position.y + event.dy;

      return { x, y };
    },
    onSwipeLeft() {
      this.$emit('swipeLeft');
    },
    onSwipeRight() {
      this.$emit('swipeRight');
    },
  },
  mounted() {
    interact(this.$refs.card).draggable({
      onmove: (event) => {
        this.position = this.getNewPosition(event);
      },
      onstart: () => {
        this.shouldAnimate = false;
      },
      onend: () => {
        this.shouldAnimate = true;

        if (this.swipeRightRatio === 1) return this.onSwipeRight();
        if (this.swipeLeftRatio === 1) return this.onSwipeLeft();

        this.position = DEFAULT_POSITION;
      },
    });
  },
};
</script>

<style scoped>
.swipe-card {
  -ms-touch-action: none;
  touch-action: none;
}

.swipe-card.animate {
  transition: transform 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.right-overlay,
.left-overlay {
  position: absolute;
  inset: 0;
  opacity: calc(var(--ratio) * 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 180px;
  pointer-events: none;
}

.right-overlay {
  background: rgba(50, 205, 50, 0.1);
}

.fa-check-circle {
  color: green;
}

.left-overlay {
  background: rgba(255, 69, 0, 0.1);
}

.fa-times-circle {
  color: red;
}

.product-name {
  font-size: 1.2rem;
  font-weight: bold;
}

/* keep card height consistent */
.card-text {
  height: 200px;
}
</style>
