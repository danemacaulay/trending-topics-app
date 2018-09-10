<template>
  <div id="app" class="container">
    <div class="row">
      <div class="col-sm text-left">
        <router-link :to="{ name: 'tweetList', query: { 'page': 1 }}">
          <img src="./assets/logo.png">
        </router-link>
      </div>
    </div>
    <masonry
      :cols="{default: 3, 1000: 3, 900: 2, 600: 1}"
      :gutter="{default: '30px', 700: '15px'}"
      >
      <div v-for="item in tweets">
        <Tweet class="twt" :id="item.id_str"></Tweet>
      </div>
    </masonry>
    <infinite-loading @infinite="getTweets"></infinite-loading>
  </div>
</template>

<script>
import { Tweet } from 'vue-tweet-embed'
import Axios from 'axios'
import InfiniteLoading from 'vue-infinite-loading';

export default {
  components: {
    Tweet,
    InfiniteLoading,
  },
  data: function () {
    return {
      tweets: [],
      page: 0,
    }
  },
  methods: {
    getTweets: function($state) {
      var that = this
      that.page++
      Axios.get('/services/tweets?page='+that.page+'&limit=9').then(function(resp) {
        that.tweets = that.tweets.concat(resp.data.tweets)
        $state.loaded();
      })
    },
  },
}
</script>

<style>
#app {
  font-family: 'Open sans', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 20px;
}

h1, h2 {
  font-weight: normal;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}
</style>
