
import { mapState } from "vuex";

export default {
  computed: mapState(["currentUser"]),
  methods: {
    isAuthorOrContributor(post) {
      const uuid = this.currentUser.uuid;
      if (post.author.uuid == uuid)
        return true;

      const contributors = post.contributors.map(({ uuid }) => uuid);
      if (contributors.includes(uuid))
        return true;

      return false;
    }
  }
}
