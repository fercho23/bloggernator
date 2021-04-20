
import moment from "moment";

export default {
  methods: {
    formatDatetime: function (value) {
      if (value) {
        return moment(String(value)).format("DD/MM/YYYY hh:mm")
      }
    }
  }
}
