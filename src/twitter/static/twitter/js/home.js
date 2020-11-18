let home = new Vue({
    el: "#home",
    data: function() {
        return {
            tweets: [],
            tweetContent: '',
            currentHandler: null,
            handlerSearchResults: [],
            hashtagSearchResults: [],
        };
    },
    methods: {
        postTweet: function(e) {
            let data = new FormData(e.target);
            axios.post('/post_tweet/', data)
            .then(res => {
                this.clearTweetForm();
            })
            .catch(err => console.log(err));
        },
        clearTweetForm: function() {
            let content = document.getElementById("content");
            content.value = '';
        },
        getChangedHandler: function(newVal, oldVal) {
            let regex = /@\w*/g
            let newMentions = [...newVal.matchAll(regex)]
            let oldMentions = [...oldVal.matchAll(regex)]

            if(newMentions.length == oldMentions.length) {
                for(let i = 0; i < newMentions.length; i++) {
                    if(newMentions[i][0] != oldMentions[i][0]) {
                        return newMentions[i];
                    }
                }
            }
        },
        getChangedHashtag: function(newVal, oldVal) {
            let regex = /#\w*/g
            let newMentions = [...newVal.matchAll(regex)]
            let oldMentions = [...oldVal.matchAll(regex)]

            if(newMentions.length == oldMentions.length) {
                for(let i = 0; i < newMentions.length; i++) {
                    if(newMentions[i][0] != oldMentions[i][0]) {
                        return newMentions[i];
                    }
                }
            }
        },
        searchHandlers: function(handler) {
            axios.get(`/search_handlers/${handler[0].slice(1)}/`,)
            .then(res => {
                this.handlerSearchResults = res.data;
            })
            .catch(err => console.log(err))
        },
        searchHashtags: function(hashtag) {
            axios.get(`/search_hashtags/${hashtag[0].slice(1)}/`,)
            .then(res => {
                this.hashtagSearchResults = res.data;
            })
            .catch(err => console.log(err))
        },
        clearHandlerSearchResults: function() {
            this.handlerSearchResults = [];
            this.currentHandler = null;
            document.getElementById("content").focus();
        },
        clearHashtagSearchResults: function() {
            this.hashtagSearchResults = [];
            this.currentHashtag = null;
            document.getElementById("content").focus();
        },
        replaceHandler: function(searchResult) {
            this.tweetContent = this.tweetContent.slice(0, this.currentHandler.index) +  
                this.tweetContent.slice(this.currentHandler.index).replace(this.currentHandler[0], `@${searchResult}`);
            this.clearHandlerSearchResults();
        },
        replaceHashtag: function(searchResult) {
            this.tweetContent = this.tweetContent.slice(0, this.currentHashtag.index) +  
                this.tweetContent.slice(this.currentHashtag.index).replace(this.currentHashtag[0], `#${searchResult}`);
            this.clearHashtagSearchResults();
        },
        getTweets: function() {
            let url = '/get_tweets/'

            if(document.location.pathname.endsWith('profile/')) {
                url = url + 'profile/'
            }
                        
            axios.get(url)
            .then(res => {
                this.tweets = res.data;
            })
            .catch(err => console.log(err))
        },
        replay: function(tweet) {},
        retweet: function(tweet) {
            if(!tweet.is_retweeted) {
                tweet.is_retweeted = true;
                tweet.retweeters_count++;
                axios.post('retweet/', {'id': tweet.id})
                .then(res => console.log(res))
                .catch(err => console.log(err))
            }
        },
        like: function(tweet) {
            if(!tweet.is_liked) {
                tweet.is_liked = true;
                tweet.likers_count++;
                axios.post('like/', {'id': tweet.id})
                .then(res => console.log(res))
                .catch(err => console.log(err))
            }
        },
        follow: function(id) {
            axios.post('/follow/', {id: id})
            .then(res => {
                console.log(res);
            })
            .catch(err => {
                console.log(err);
            })
        }
    },
    mounted: function() {
        axios.defaults.headers['X-CSRFToken'] = Cookies.get('csrftoken');
        this.getTweets();
    },
    watch: {
        tweetContent: function(newVal, oldVal) {
            let handler = this.getChangedHandler(newVal, oldVal);
            let hashtag = this.getChangedHashtag(newVal, oldVal);
            
            if(handler) {
                this.searchHandlers(handler);
                this.currentHandler = handler;
            } else if(this.handlerSearchResults.length > 0) {
                this.clearHandlerSearchResults();
            }

            if(hashtag) {
                this.searchHashtags(hashtag);
                this.currentHashtag = hashtag;
            } else if(this.hashtagSearchResults.length > 0) {
                this.clearHashtagSearchResults();
            }
        }
    },
});