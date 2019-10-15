<template>
  <div class="post_container col-md-12">
    <div class="post_elem" v-for="post in posts" v-bind:key="post.id">
        <a href="javascript:void(0)" v-on:click="openInModal(post)"><h3 class="post_title">{{ post.title }}</h3></a>
        <span class="post_text">{{ longText(post.text) }}</span>
      <div class="post_vote">
        <img v-on:click="vote_good(post.pk)" v-bind:style="{ opacity: isLiked(post.is_voted) ? '0.5' : '1'  }" class="post_good" src="~assets/images/youtube-like.png">
        {{ post.rating }}
        <img v-on:click="vote_bad(post.pk)" v-bind:style="{ opacity: isDisliked(post.is_voted) ? '0.5' : '1'  }" class="post_bad" src="~assets/images/youtube-dislike.png">
      </div>
    </div>

    <v-dialog height="auto" :scrollable="true" :adaptive="true"/>
  </div>
</template>

<script>
  import axios from 'axios'

  export default {
    name: "PostList",
    mounted() {
      this.get_posts()
    },
    data() {
      return {
        posts: {},
      }
    },
    methods: {
      isLiked(vote) {
        return vote === 1;
      },
      isDisliked(vote) {
        return vote === -1;
      },
      openInModal(post) {
        this.$modal.show('dialog', {
          title: post.title,
          text: post.text,
        })
      },
      longText(text) {
        if (text.length > 329) return text.substring(0, 329) + '...';
        else return text;
      },
      get_posts() {
        this.posts = [];
        axios.get("http://localhost:8000/posts/", { headers: {"Authorization": `Bearer ${this.$store.state.localStorage.token}` }, crossdomain: true})
          .then(response => {
            for (let obj of response.data) {
              this.posts.push(obj)
            }
          })
          .catch(error => {
            if (error.response.status === 401) {
                this.$store.commit('localStorage/removeUser');
            }
            else console.log(error)
          })
      },
      vote_good(post_pk) {
        axios.post("http://localhost:8000/votes/", {post: post_pk, author: this.$store.state.localStorage.user.pk, vote: 1}, { headers: {"Authorization": `Bearer ${this.$store.state.localStorage.token}` }, crossdomain: true})
          .then(response => {
            if (response.status === 200) {
                this.posts.find(x => x.pk === post_pk).rating++;
                this.posts.find(x => x.pk === post_pk).rating++;
                this.posts.find(x => x.pk === post_pk).is_voted = 1;
            } else if (response.status === 202) {
              this.posts.find(x => x.pk === post_pk).rating--;
              this.posts.find(x => x.pk === post_pk).is_voted = 0;
            } else {
                this.posts.find(x => x.pk === post_pk).rating++;
                this.posts.find(x => x.pk === post_pk).is_voted = 1;
            }
          })
          .catch(error => {
            alert(error);
          });
      },
      vote_bad(post_pk) {
        axios.post("http://localhost:8000/votes/", {post: post_pk, author: this.$store.state.localStorage.user.pk, vote: -1}, { headers: {"Authorization": `Bearer ${this.$store.state.localStorage.token}` }, crossdomain: true})
          .then(response => {
            if (response.status === 200) {
              this.posts.find(x => x.pk === post_pk).rating--;
              this.posts.find(x => x.pk === post_pk).rating--;
              this.posts.find(x => x.pk === post_pk).is_voted = -1;
            } else if (response.status === 202) {
              this.posts.find(x => x.pk === post_pk).rating++;
              this.posts.find(x => x.pk === post_pk).is_voted = 0;
            } else {
                this.posts.find(x => x.pk === post_pk).rating--;
                this.posts.find(x => x.pk === post_pk).is_voted = -1;
            }
          })
          .catch(error => {
            alert(error);
          });
      }
    }
  }
</script>

<style scoped>
  .post_container {
    display: flex;
    flex-wrap: wrap;
    justify-content: start;
  }

  .post_elem {
    height: 300px;
    width: 300px;
    background-color: gold;
    margin: 15px;
    display: flex;
    flex-direction: column;
  }

  .post_title {
    text-align: center;
    padding-bottom: 15px;
  }

  .post_text {
    flex-grow: 1;
    padding: 10px;
  }

  .post_vote {
    align-self: flex-end;
    justify-self: flex-end;
    padding: 10px;
  }

  .post_good {
    width: 15px;
    height: 15px;
    cursor: pointer;
  }

  .post_bad {
    width: 15px;
    height: 15px;
    cursor: pointer;
  }

</style>
