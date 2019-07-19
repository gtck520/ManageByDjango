import json from '@/json'
export default{
	data: {
		tabBars: [],
		tabCurrentIndex: 0,
	},
	
	methods: {
		loadTabbars(){
			let tabList = json.tabList;
			tabList.forEach(item=>{
				item.newsList = [];
				item.loadMoreStatus = 0;  //加载更多 0加载前，1加载中，2没有更多了
				item.refreshing = 0;
			})
			this.tabBars = tabList;
			this.loadNewsList('add');
		},
		//新闻列表
		loadNewsList(type){
			let tabItem = this.tabBars[this.tabCurrentIndex];
			
			//type add 加载更多 refresh下拉刷新
			if(type === 'add'){
				if(tabItem.loadMoreStatus === 2){
					tabItem.loadMoreStatus = 1
					setTimeout(() => {
						tabItem.loadMoreStatus = 2;
					}, 100)
					return;
				}
				tabItem.loadMoreStatus = 1;
			}
			// #ifdef APP-PLUS
			else if(type === 'refresh'){
				tabItem.refreshing = true;
			}
			// #endif
			
			//setTimeout模拟异步请求数据
			setTimeout(()=>{
				let list = json.newsList;
				list.sort((a,b)=>{
					return Math.random() > .5 ? -1 : 1; //静态数据打乱顺序
				})
				if(type === 'refresh'){
					tabItem.newsList = []; //刷新前清空数组
				}
				list.forEach(item=>{
					tabItem.newsList.push(item);
				})
				//下拉刷新 关闭刷新动画
				if(type === 'refresh'){
					this.$refs.mixPulldownRefresh && this.$refs.mixPulldownRefresh.endPulldownRefresh();
					// #ifdef APP-PLUS
					tabItem.refreshing = false;
					// #endif
					tabItem.loadMoreStatus = 0;
				}
				//上滑加载 处理状态
				if(type === 'add'){
					tabItem.loadMoreStatus = tabItem.newsList.length > 40 ? 2: 0;
				}
			}, 600)
		},
		//新闻详情
		navToDetails(item){
			let data = {
				id: item.id,
				title: item.title,
				author: item.author,
				time: item.time
			}
			let url = item.videoSrc ? 'videoDetails' : 'details'; 
			uni.navigateTo({
				url: `/pages/details/${url}?data=${JSON.stringify(data)}`
			})
		},
	}
	
}