let home = new Vue({
    el: "#home",
    data: function() {
        return {
            tweets: [],
            tweetContent: '',
            currentHandler: null,
            handlerSearchResults: [],
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
                        return newMentions[i];
                    }
                }
            }
        },
        searchHandlers: function(handler) {
            axios.get(`/search_handlers/${handler[0].slice(1)}/`,)
            .then(res => {
                console.log(res.data);
                this.handlerSearchResults = res.data;
            })
            .catch(err => console.log(err))
        },
        clearHandlerSearchResults: function() {
            this.handlerSearchResults = [];
            this.currentHandler = null;
            document.getElementById("content").focus();
        },
        replaceHandler: function(searchResult) {
            this.tweetContent = this.tweetContent.slice(0, this.currentHandler.index) +  
                this.tweetContent.slice(this.currentHandler.index).replace(this.currentHandler[0], `@${searchResult}`);
            this.clearHandlerSearchResults();
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
                this.currentHandler = handler;
            } else if(this.handlerSearchResults.length > 0) {
                this.clearHandlerSearchResults();
            }
        }
    },
});