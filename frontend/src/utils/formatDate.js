
import moment from 'moment';

export default {
  methods: {
    formatDate: function (value) {
      if (value) {
        return moment(String(value)).format('DD/MM/YYYY');
      }
    }
  }
}
