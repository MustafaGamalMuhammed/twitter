let home = new Vue({
    el: "#home",
    data: function() {
        return {
            tweets: [],
            tweetContent: '',
        };
    },
    methods: {
        postTweet: function(e) {
            let data = new FormData(e.target);
            axios.post('post_tweet/', data)
            .then(res => {
                console.log(res);
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
                        return newMentions[i][0].slice(1);
                    }
                }
            }
        },
        searchHandlers: function(handler) {
            axios.get(`/search_handlers/${handler}/`,)
            .then(res => {
                console.log(res.data);
            })
            .catch(err => console.log(err))
        }
    },
    mounted: function() {
        axios.defaults.headers['X-CSRFToken'] = Cookies.get('csrftoken');
    },
    watch: {
        tweetContent: function(newVal, oldVal) {
            let handler = this.getChangedHandler(newVal, oldVal);
        
            if(handler) {
                this.searchHandlers(handler);
            }
        }
    },
});