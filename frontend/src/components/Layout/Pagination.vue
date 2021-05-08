<template>
  <nav>
    <ul class="pagination justify-content-center mt-2">
        <li class="page-item " :class="{ disabled: !page.url}" v-for="(page, index) in pages" :key="index">
          <router-link
            class="page-link"
            :to="page.url">
            {{ page.number }}
          </router-link>
        </li>
    </ul>
  </nav>
</template>

<script>
  export default {
    name: "Pagination",
    props: {
      baseUrl: {
        type: String,
        default: window.location.pathname
      },
      query: {},
      pageCount: {
        type: Number,
        default: 0
      },
      previousUrl: {
        type: String,
        default: ""
      },
      nextUrl: {
        type: String,
        default: ""
      },
      elementsByPage: {
        type: Number,
        default: 10
      },
      numberPagesEachSide: {
        type: Number,
        default: 4
      },
      firstPageNumber: {
        type: Number,
        default: 1
      },
      propPageOnUrl: {
        type: String,
        default: "page"
      },
    },

    mounted() {
      this.generatePages();
    },

    data() {
      return {
         pages: [],
         currentPageNumber: 0,
      };
    },

    methods: {
      generatePages() {
        if (this.query || this.previousUrl || this.nextUrl) {
          this.pages = [];
          this.currentPageNumber = this.query[this.propPageOnUrl] ? parseInt(this.query[this.propPageOnUrl], 10) : this.firstPageNumber;
          // console.log('generatePages ' + this.currentPageNumber);

          const base_url = this.baseUrl;

          let start_page = this.currentPageNumber - this.numberPagesEachSide;
          let end_page = this.currentPageNumber + this.numberPagesEachSide;
          const page_total_amount = Math.ceil(this.pageCount / this.elementsByPage);

          if (start_page <= 0) {
              start_page = this.firstPageNumber;
          }

          if (end_page > page_total_amount) {
              end_page = page_total_amount;
          }

          // PREV PAGE
            if (this.previousUrl) {
              this.pages.push({
                "url": base_url + (this.previousUrl.includes("?") ? "?" + this.previousUrl.split("?")[1] : ""),
                "number": "Previous",
              });
            }
          // -- PREV PAGE

          // FIRST PAGE
            if (start_page > this.firstPageNumber) {
              let query = Object.assign({}, this.query);
                query[this.propPageOnUrl] = this.firstPageNumber;

              this.pages.push({
                "url": {
                  path: base_url,
                  query: query,
                },
                "number": this.firstPageNumber,
              });

              if (start_page > (this.firstPageNumber + 1)) {
                this.pages.push({
                  "url": "",
                  "number": "...",
                });
              }
            }
          // -- FIRST PAGE

          // OTHERS PAGES
            for (let page = start_page; page <= end_page; page++) {
              let query = Object.assign({}, this.query);
                query[this.propPageOnUrl] = page;

              let page_data = {};
                page_data.number = page;
                page_data.url = "";
              if (page != this.currentPageNumber) {
                page_data.url = {
                  path: base_url,
                  query: query,
                };
              }
              this.pages.push(page_data);
            }
          // -- OTHERS PAGES

          // LAST PAGE
            if (end_page < page_total_amount) {
              if (end_page < (page_total_amount - this.firstPageNumber)) {
                this.pages.push({
                  "url": "",
                  "number": "...",
                });
              }

              let query = Object.assign({}, this.query);
                query[this.propPageOnUrl] = page_total_amount;

              this.pages.push({
                "url": {
                  path: base_url,
                  query: query,
                },
                "number": page_total_amount,
              });
            }
          // -- LAST PAGE

          // NEXT PAGE
            if (this.nextUrl) {
              this.pages.push({
                "url": base_url + (this.nextUrl.includes("?") ? "?" + this.nextUrl.split("?")[1] : ""),
                "number": "Next",
              });
            }
          // -- NEXT PAGE
        }
      }
    }
  }
</script>
