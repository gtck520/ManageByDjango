<template>
	<view>
		<cu-custom bgImage="../../static/img/sylb2244.jpg" :isBack="true">
			<block slot="backText">返回</block>
			<block slot="content">经文搜索</block>
		</cu-custom>
		<view class="cu-bar bg-white search fixed" :style="[{top:CustomBar + 'px'}]">
			<view class="search-form round">
				<text class="cuIcon-search"></text>
				<input type="text" placeholder="输入搜索的关键词" confirm-type="search" v-model="searchstr"></input>
			</view>
			<view class="action">
				<button class="cu-btn bg-gradual-green shadow-blur round" @tap="getSearch()">搜索</button>
			</view>
		</view>
		<view class="cu-bar bg-white solid-bottom margin-top">
			<view class="action">
				<text class="cuIcon-title text-orange "></text> 搜索结果
			</view>
		</view>
		<view class="my-list">
			<view class="my-item" v-for="(item,index) in searchlist" :key="index">
				<!--<view class="my-avatar round lg "><view class="text-sm">{{item.VolumeSN.ShortName}}</view></view> -->
				<view class="my-content">
					<view class="text-grey">{{item.VolumeSN.FullName}}</view>
					<view class="text-gray text-sm flex ">
						<rich-text :nodes="item.content"></rich-text>
						<!-- <rich-text :nodes="nodes"></rich-text> -->
					</view>
				</view>
<!-- 				<view class="action">
					<view class="text-grey text-xs">22:20</view>
					<view class="cu-tag round bg-grey sm">5</view>
				</view> -->
			</view>
		</view>

	</view>
</template>

<script>
	export default {
		data() {
			return {
				StatusBar: this.StatusBar,
				CustomBar: this.CustomBar,
				searchstr:'',
				searchlist:[],
				page: 1,				// 当前第几页
				totalPages: 1			,// 总页数
				loading:false

			}
		},
		onLoad() {

		},
		onReachBottom() {
			var page = this.page + 1;	
			this.getSearch(page);
		},
		methods: {
			getSearch(pagea){
				var isPage=false;//是否翻页
				var page = this.page;
				// 搜索内容
				if (pagea != null && pagea != "" && pagea != undefined) {
				var page = pagea;
				isPage = true;
				}
				
				uni.showLoading({
					mask: true,
					title: "请稍后..."
				});
				uni.showNavigationBarLoading();
				
				this.loading = true
				this.$api.getSearch(this.searchstr,page,{noncestr: Date.now()}).then((res)=>{
					this.loading = false;
					var searchlist = res.data.results;
					if(isPage){
						this.searchlist = this.searchlist.concat(searchlist);
					}else{
						this.searchlist = searchlist;
					}
					
					this.totalPages = res.data.count;	// 获取总页数
					this.page = page;		// 覆盖当前页面里的page
					console.log(this.searchlist);
					//隐藏加载框
					uni.hideNavigationBarLoading();
					uni.hideLoading();
				}).catch((err)=>{
					this.loading = false;
					console.log('request fail', err);
				});
			}
		}
		// ,
		// filters: {
		//   redSearch: function (value,searchstr) {
		// 	var newsearch = '<view class="text-red">'+searchstr+'</view>';
		// 	var str=value.replace(searchstr,newsearch);
		// 	console.log(str);
		// 	return str;
		//   }
		// }
	}
</script>

<style>
.my-list{
	display: flex;
	flex-direction: column;
}
.my-item{
	display: flex;
	flex-direction: row;
	background-color: #ffffff;
	border-bottom: 6upx solid rgba(0, 0, 0, 0.05);
}
.my-content{	
	width: 100%;
	line-height: 1.6em;
	padding: 20upx;
}
</style>
