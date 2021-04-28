
import { mapState } from "vuex";

export default {
  computed: mapState(["currentUser"]),
  methods: {
    isAuthorOrContributor(post) {
      if (this.currentUser) {
        const uuid = this.currentUser.uuid;
        if (post.author && post.author.uuid == uuid)
          return true;

        if (post.contributors) {
          const contributors = post.contributors.map(({ uuid }) => uuid);
          if (contributors.includes(uuid))
            return true;
        }
      }

      return false;
    }
  }
}
