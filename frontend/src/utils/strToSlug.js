
export default {
  methods: {
    strToSlug(value) {
      let slug = '';
      if (value) {
        // Change to lower case
        slug = value.toLowerCase();

        // Letter 'a'
        slug = slug.replace(/a|á|à|ã|ả|ạ|ă|ắ|ằ|ẵ|ẳ|ặ|â|ấ|ầ|ẫ|ẩ|ậ/gi, 'a');

        // Letter 'e'
        slug = slug.replace(/e|é|è|ẽ|ẻ|ẹ|ê|ế|ề|ễ|ể|ệ/gi, 'e');

        // Letter 'i'
        slug = slug.replace(/í|ì|î/gi, 'i');

        // Letter 'o'
        slug = slug.replace(/o|ó|ò|õ|ỏ|ọ|ô|ố|ồ|ỗ|ổ|ộ|ơ|ớ|ờ|ỡ|ở|ợ/gi, 'o');

        // Letter 'u'
        slug = slug.replace(/u|ú|ù|ũ|ủ|ụ|ư|ứ|ừ|ữ|ử|ự/gi, 'u');

        // Letter 'i'
        slug = slug.replace(/ç/gi, 'c');

        // Letter 'd'
        slug = slug.replace(/đ/gi, 'd');

        // Trim the last whitespace
        slug = slug.replace(/\s*$/g, '');

        // Change whitespace to '-'
        slug = slug.replace(/\s+/g, '-');
      }

      return slug;
    }
  }
}
