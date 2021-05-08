<template>
  <div class="autocomplete">
    <input class="form-control" type="text"
      v-model="search" 
      @input="onChange" 
      @keydown.down="onArrowDown" 
      @keydown.up="onArrowUp" 
      @keydown.enter.prevent="onEnter"
    />
    <transition name="slide-fade">
      <ul ref="scrollContainer" id="autocomplete-results" v-if="isOpen" class="autocomplete-results">
        <li class="loading" v-if="isLoading">
          Loading results...
        </li>
        <li ref="options" v-else v-for="(result, index) in results" :key="index" 
          @click="setResult(result)" 
          class="autocomplete-result" 
          :class="{ 'is-active': index === arrowCounter }">
          {{ result[propToShow] }}
        </li>
      </ul>
    </transition>
  </div>
</template>

<script>
  export default {
    name: 'AutoComplete',
    props: {
      api: null,
      functionAfter: null,
      propToShow: {
        type: String,
        default: 'name'
      },
      propToGetApiResults: {
        type: String,
        default: 'results'
      },
    },

    data() {
      return {
         isOpen: false,
         results: [],
         search: '',
         isLoading: false,
         arrowCounter: 0,
      };
    },

    mounted() {
      document.addEventListener('click', this.handleClickOutside);
    },
    destroyed() {
      document.removeEventListener('click', this.handleClickOutside);
    },

    methods: {
      onChange() {
        if (this.api != null) {
          this.isLoading = true;
          this.isOpen = true;

          this.api(this.search).then(response => {
            this.results = this.propToGetApiResults === '' ? response.data : response.data[this.propToGetApiResults];
          })
          .finally(() => {
            this.isLoading = false
          });
        } else {
          this.isOpen = true;
        }
      },

      setResult(resultSelected) {
        this.completeItem = resultSelected;
        this.search = '';
        this.isOpen = false;
        this.$emit('input', this.search);
        if (this.functionAfter) {
          this.functionAfter(resultSelected);
        }
      },

      fixScrolling() {
        if (this.$refs.options[this.arrowCounter]) {
          const height = this.$refs.options[this.arrowCounter].clientHeight;
          this.$refs.scrollContainer.scrollTop = height * this.arrowCounter;
        }
      },

      onArrowDown(event) {
        event.preventDefault();
        if (this.arrowCounter < (this.results.length - 1)) {
          this.arrowCounter = this.arrowCounter + 1;
          this.fixScrolling();
        }
      },
      onArrowUp() {
        event.preventDefault();
        if (this.arrowCounter > 0) {
          this.arrowCounter = this.arrowCounter - 1;
          this.fixScrolling();
        }
      },
      onEnter() {
        this.setResult(this.results[this.arrowCounter]);
        this.arrowCounter = -1;
      },
     // this will close the drop-down section when the user click some where// out side of the component
      handleClickOutside(event) {
        if (!this.$el.contains(event.target)) {
          this.isOpen = false;
          this.arrowCounter = -1;
        }
      }
    }

  }
</script>

<style scoped>
  .autocomplete {
    position: relative;
  }

  .autocomplete-results {
    z-index: 1000;
    position: absolute;
    padding: 0;
    margin: 0;
    border: 1px solid rgb(186, 206, 228);
    border-radius: 4px;
    max-height: 120px;
    overflow: auto;
    width: 100%;
    background-color: white;
  }

  .autocomplete-result {
    list-style: none;
    text-align: left;
    padding: 4px 2px;
    cursor: pointer;
    background-color: white;
  }

  .autocomplete-result.is-active,
  .autocomplete-result:hover {
    background-color: #4AAE9B;
    color: white;
  }

  .slide-fade-enter-active {
    transition: all .2s ease;
  }
  .slide-fade-leave-active {
    transition: all .4s cubic-bezier(1.0, 0.5, 0.8, 1.0);
  }
  .slide-fade-enter, .slide-fade-leave-to {
    transform: translateX(10px);
    opacity: 0;
  }
</style>