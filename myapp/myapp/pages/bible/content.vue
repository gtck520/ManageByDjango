<template>
	<view>
		<cu-custom bgColor="bg-gradual-blue" :isBack="true">
			<block slot="content">{{fullname}}</block>
			</cu-custom>
		<view class="cu-bar bg-white solid-bottom margin-top">
			<view class="action">
				<text class="cuIcon-title text-blue"></text>{{ChapterSN}}
			</view>
		</view>
		<scroll-view class="padding bg-white" scroll-y scroll-with-animation style="height:calc(100vh - 250upx)" >
			<view class="text-left padding" v-for="(item,index) in contentlist" :key="index" :id="'main-'+item.VerseSN" >
				<view class='cu-tag round'>{{item.VerseSN}}</view>
				{{item.Lection}}
			</view>
		</scroll-view>
	</view>
	
</template>

<script>
	export default {
		data() {
			return {
				booksn:1,
				versesn:1,
				chaptersn:1,
				contentlist:{},
				fullname:'',
				ChapterSN:''
			}
		},
		onLoad(o) {
			this.booksn = o.booksn;
			this.chaptersn = o.chaptersn;
			this.versesn = o.versesn;
			this.getcontents(o.booksn,o.chaptersn);
		},
		methods: {
			getcontents(booksn,chaptersn){
				// 获取节列表
				uni.request({
				url: this.ApiHost+'v1/contents/'+booksn+'/'+chaptersn+'/',
				data: {},
				method: 'GET',
				}) .then(data => {
					var [error, res]  = data;
					this.contentlist = res.data;
					this.ChapterSN=res.data[0]['ChapterSN']
					this.fullname=res.data[0]['VolumeSN'].FullName;
					//console.log(this.contentlist);
				});
			}
		}
	}
</script>

<style>

</style>
