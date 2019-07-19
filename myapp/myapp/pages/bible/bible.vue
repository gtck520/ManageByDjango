<template>
	<view >		
		<scroll-view scroll-x class="bg-white nav">
			<view class="flex text-center">
				<view class="cu-item flex-sub" :class="index==TabCur?'text-orange cur':''" v-for="(item,index) in tabbars" :key="index" @tap="tabSelect" :data-id="index">
					{{item}}
				</view>
			</view>
		</scroll-view>		
		<block v-if="TabCur==0">
			<view class="grid col-4 padding-sm">
				<view class="padding-sm" v-for="(item,index) in bookslist" :key="index" @tap="getChapters" :data-booksn="item.SN">
					<view class="padding radius text-center shadow-blur bg-cyan" >
						<view class="text-lg">{{item.ShortName}}</view>
						<view class="margin-top-sm smalltext">{{item.FullName}}</view>
					</view>
				</view>
			</view>
		</block>	
		<block v-if="TabCur==1">
			<view class="cu-list grid col-5">
				<view class="cu-item" v-for="(item,index) in chapterslist" :key="index" @tap="getVerses" :data-chaptersn="item.ChapterSN">
					<text>{{item.ChapterSN}}</text>
				</view>
			</view>
		</block>	
		<block v-if="TabCur==2">
			<view class="cu-list grid col-5">
				<view class="cu-item" v-for="(item,index) in verseslist" :key="index" @tap="goContent" :data-booksn="item.VolumeSN_id" :data-chaptersn="item.ChapterSN" :data-versesn="item.VerseSN">
					<text>{{item.VerseSN}}</text>
				</view>
			</view>
		</block>
	</view>
</template>

<script>
export default {
	data() {
		return {
			ColorList: this.ColorList,
			bookslist:{},
			chapterslist:{},
			verseslist:{},
			booksn:1,
			tabbars:{
				0:'卷',
				1:'章',
				2:'节'
			},
			TabCur: 0,
			scrollLeft: 0,
			cuIcon: [{
				name: 'appreciate',
				isShow: true
			}, {
				name: 'check',
				isShow: true
			}, {
				name: 'close',
				isShow: true
			}, {
				name: 'edit',
				isShow: true
			}, {
				name: 'emoji',
				isShow: true
			}, {
				name: 'favorfill',
				isShow: true
			}]
		};
	},
	onLoad() {
		//初始化各信息
		this.getVolume();
		this.getChapters(null);
		this.getVerses(null);
	},
	methods: {
		outBtn: function(){
			// 清除缓存
			uni.clearStorage();
			// 两秒后重启
			setTimeout(function() {
				plus.runtime.restart();
			}, 2000);
		},
		tabSelect(e) {
			this.TabCur = e.currentTarget.dataset.id;
			this.scrollLeft = (e.currentTarget.dataset.id - 1) * 60
		},
		getVolume(){
			// 获取卷列表
			uni.request({
			url: this.ApiHost+'v1/books/',
			data: {},
			method: 'GET',
			}) .then(data => {
				var [error, res]  = data;
				this.bookslist = res.data;
			})
		},
		getChapters(e){
			if(e != null && e != "" && e != undefined){
				var booksn = e.currentTarget.dataset.booksn;
				e.currentTarget.dataset.id=1;
				this.booksn = booksn;
			}else{
				var booksn = this.booksn;//初始化时默认加载 第一卷
			}
			// 获取章列表
			uni.request({
			url: this.ApiHost+'v1/books/'+booksn+'/chapters/',
			data: {},
			method: 'GET',
			}) .then(data => {
				var [error, res]  = data;
				this.chapterslist = res.data;
				if(e != null && e != "" && e != undefined){
				this.tabSelect(e);
				}
				
			});
		},
		getVerses(e){
			if(e != null && e != "" && e != undefined){
				var chaptersn = e.currentTarget.dataset.chaptersn;
				e.currentTarget.dataset.id=2;
			}else{
				var chaptersn = 1;
			}
			// 获取节列表
			uni.request({
			url: this.ApiHost+'v1/books/'+this.booksn+'/chapters/'+chaptersn+'/',
			data: {},
			method: 'GET',
			}) .then(data => {
				var [error, res]  = data;
				this.verseslist = res.data;
				if(e != null && e != "" && e != undefined){
				this.tabSelect(e);
				}
				//console.log(this.verseslist)
			});
		},
		goContent(e){	
            //localStorage.setItem("versesn",e.currentTarget.dataset.versesn);     
			uni.setStorageSync("versesn", e.currentTarget.dataset.versesn);
			uni.navigateTo({
				url:"content?booksn="+e.currentTarget.dataset.booksn+"&chaptersn="+e.currentTarget.dataset.chaptersn+"&versesn="+e.currentTarget.dataset.versesn
			});
		}
	}
};
</script>

<style>
	.smalltext{		
		font-size: 9px;
	}
</style>
