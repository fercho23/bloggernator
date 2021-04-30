
import { mapState } from "vuex";

export default {
  computed: mapState(["currentUser"]),
  methods: {
    isOwnerInCommunity(community) {
      if (this.currentUser) {
        const uuid = this.currentUser.uuid;
        if (community.owner.uuid == uuid)
          return true;
      }

      return false;
    }
  }
}
