<template>
  <div className="container">
    <div class="location-item px-1 text-left align-self-stretch d-flex align-items-stretch text-decoration-none">
      <div class="p-3">
        <h1 @click="onClickLocation(location)">{{ location.Name }}</h1>
        <div>
          <p v-for="item in location.Address" :key="item">{{ item }}</p>
        </div>
        <a :href="`tel:${location.Phone}`"><i class="fas fa-phone"></i></a>
        <i @click="onClickDirections(location)" class="fas fa-directions"></i>
        <h2 @click="toggleHours()">Hours</h2>
        <div class="hours" :class="{ 'show-hours': isShowHours }">
          <p v-for='item in location["Business Hours"]' :key="item">{{ item }}</p>
        </div>
        <h2 @click="toggleBeerList()">Beer list</h2>
        <div class="beer-list" :class="{ 'show-beer-list': isShowBeerList }">
          <p v-for="(item, index) in location.Beers" :key="index">{{ item }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LocationDetail',
  props: {
    location: {
      required: false,
    },
    changeViewport: null,
    showDirections: null
  },
  data() {
    return {
      isShowHours: false,
      isShowBeerList: false
    };
  },
  methods: {
    onClickLocation(location) {
      this.changeViewport(location);
    },
    onClickDirections(location) {
      this.showDirections(location);
    },
    toggleHours() {
      this.isShowHours = !this.isShowHours;
    },
    toggleBeerList() {
      this.isShowBeerList = !this.isShowBeerList;
    }
  }
};
</script>

<style scoped>
h1 {
  font-size: 1em;
}

h2 {
  font-size: .8em;
}

p {
  font-size: .9em;
  margin-bottom: 0;
}

a {
  color: inherit;
}

.hours, .beer-list {
  display: none;
}

.show-hours, .show-beer-list {
  display: block;
}

.fas {
  margin: 10px;
}
</style>
