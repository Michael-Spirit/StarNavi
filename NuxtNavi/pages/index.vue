<template>
  <div>
    <modal name="new-post">
      <form>
        <div class="new-post-div">
          <div>
            <label for="title">Title</label>
            <input v-model="post.title" id="title" placeholder="title">
          </div>
          <div>
            <label for="text">Text</label>
            <textarea v-model="post.text" rows="10" style="width: -webkit-fill-available" id="text" placeholder="text"></textarea>
          </div>
          <div style="text-align: right">
            <button v-on:click="newPost()" type="button">Submit</button>
          </div>
        </div>
      </form>
    </modal>


    <div class="header" v-if="$store.state.localStorage.is_authenticated === true">
      <a href="#" class="logo">Hello {{ $store.state.localStorage.user.username }}</a>
      <div class="header-right">
        <a class="active" href="javascript:void(0)" v-on:click="show_modal()">Create Post</a>
        <a href="javascript:void(0)" v-on:click="vLogout()">Logout</a>
      </div>
    </div>

  <section class="container" v-else>
    <div>
      <client-only>
        <login-form/>
      </client-only>
    </div>
  </section>

    <div v-if="$store.state.localStorage.is_authenticated === true">
      <post-list ref="postList"></post-list>
    </div>

  </div>
</template>

<script>
import axios from 'axios'

export default {
  components: {
    'login-form': () => import('@/components/LoginForm.vue'),
    'post-list': () => import('@/components/PostList.vue')
  },
  data() {
    return {
      post: {
        title: '',
        text: '',
        author: '',
      }
    }
  },
  methods: {
    vLogout() {
      axios.post("http://localhost:8000/rest-auth/logout/", { crossdomain: true })
        .then(() => {this.$store.commit('localStorage/removeUser');})
        .catch(error => {console.log('error:', error)})
    },
    show_modal() {
      this.$modal.show('new-post');
    },
    close_modal() {
      this.$modal.hide('new-post');
    },
    newPost() {
      axios.post("http://localhost:8000/posts/", this.post, { headers: {"Authorization": `Bearer ${this.$store.state.localStorage.token}` }, crossdomain: true})
        .then(response => {
          this.close_modal();
          this.$refs.postList.get_posts();
        })
        .catch(error => {
          alert(error)
        })
    }
  },
  mounted() {
    if (this.$store.state.localStorage.user === null) {
        this.vLogout();
    }
    else this.post.author = this.$store.state.localStorage.user.pk;
  }
}
</script>

<style>
  .container {
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
  }

  .title {
    font-family: "Quicksand", "Source Sans Pro", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; /* 1 */
    display: block;
    font-weight: 300;
    font-size: 100px;
    color: #35495e;
    letter-spacing: 1px;
  }

  .subtitle {
    font-weight: 300;
    font-size: 42px;
    color: #526488;
    word-spacing: 5px;
    padding-bottom: 15px;
  }

  .links {
    padding-top: 15px;
  }

  * {
    box-sizing: border-box;
  }

  body {
    margin: 0;
    font-family: Arial, Helvetica, sans-serif;
  }

  .header {
    overflow: hidden;
    background-color: #f1f1f1;
    padding: 20px 10px;
  }

  .header a {
    float: left;
    color: black;
    text-align: center;
    padding: 12px;
    text-decoration: none;
    font-size: 18px;
    line-height: 25px;
    border-radius: 4px;
  }

  .header a.logo {
    font-size: 25px;
    font-weight: bold;
  }

  .header a:hover {
    background-color: #ddd;
    color: black;
  }

  .header a.active {
    background-color: dodgerblue;
    color: white;
  }

  .header-right {
    float: right;
  }

  .new-post-div {
    padding: 15px;
  }
  .new-post-div div {
    margin-bottom: 15px;
    margin-top: 15px;
  }


@media screen and (max-width: 500px) {
  .header a {
    float: none;
    display: block;
    text-align: left;
  }

  .header-right {
    float: none;
  }


}
</style>

