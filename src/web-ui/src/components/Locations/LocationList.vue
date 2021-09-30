<template>
  <div className="container">
    <h1>Locations</h1>

    <LoadingFallback v-if="isLoading" class="col my-4 text-center"></LoadingFallback>
    <div v-else
      v-for="location in locations" :key="location.Id"
    >
        <div class="location-item px-1 text-left align-self-stretch d-flex align-items-stretch text-decoration-none">
          <div class="p-3">
            <h1 @click="onClickLocation(location)">{{ location.Name }}</h1>
            <div>
              <p v-for="item in location.Address" :key="item">{{ item }}</p>
            </div>
            <i class="fas fa-phone"></i>
            <i class="fas fa-directions"></i>
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
  </div>
</template>

<script>
import LoadingFallback from '@/components/LoadingFallback/LoadingFallback';

export default {
  name: 'LocationList',
  props: {
    locations: {
      type: Array,
      required: false,
    },
    changeViewport: null,
  },
  data() {
    return {
      isShowHours: false,
      isShowBeerList: false
    };
  },
  components: {
    LoadingFallback,
  },
  computed: {
    isLoading() {
      return !this.locations;
    },
  },
  methods: {
    onClickLocation(location) {
      this.changeViewport(location);
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
.location-item h1 {
  font-size: 1em;
}

.location-item h2 {
  font-size: .8em;
}

.location-item p {
  font-size: .9em;
  margin-bottom: 0;
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
