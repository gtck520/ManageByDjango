<template>
	<view>
		<view id="top-box" class="cu-bar bg-white solid-bottom">
			<view class="action text-black">
				<text v-if="currentType===1">判断题</text>
				<text v-else-if="currentType===2">单选题</text>
				<text v-else-if="currentType===3">多选题</text>
				<text v-else-if="currentType===4">填空题</text>
				<text v-else-if="currentType===5">问答题</text>
			</view>
			<view class="action">
				<button class="cu-btn bg-green shadow" @tap="showCardModal" data-target="modalCard">答题卡</button>
			</view>
		</view>
		<view class="cu-modal" :class="modalCard=='modalCard'?'show':''" @tap="hideCardModal">
			<view class="cu-dialog" @tap.stop>
				
				<scroll-view class="page padding" :scroll-y=true :style="{'height':swiperHeight}" >				
				<view class="cu-bar solid-bottom">
					<view class="action">
						<text class="cuIcon-title text-red"></text>答题卡
					</view>					
				</view>
				<view class="grid col-5 ">
					<view class="margin-tb-sm text-center" v-for="(subject,index) in subjectList" :key="index">
						<button class="cu-btn round" :class="[subject.userAnswer.length===0?'line-grey':'bg-red']" @click="AppointedSubject(index)" >{{index+1}}</button>
					</view>
				</view>
				
				</scroll-view>
			</view>
		</view>
		<view class="cu-modal padding " :class="modalError=='modalError'?'show':''" @tap="hideErrorModal">
			<view class="cu-dialog bg-white" @tap.stop>								
				
				<view class="cu-bar solid-bottom ">
					<view class="action">
						<text class="cuIcon-title text-red"></text>试题纠错
					</view>					
				</view>
				
				<radio-group class="block" >
					<view class="cu-list menu text-left">
					<view class="cu-item cu-item-error" v-for="error in errorList" >
						<radio :value="error"></radio>
						<view class="title text-black margin-left">{{error}}</view>
					</view>	
					</view>	
				</radio-group>				
				
				<view class="padding flex flex-direction ">				
					<button class="cu-btn bg-red margin-tb-sm lg" @click="SubmitError">提 交</button>
				</view>
			</view>
		</view>
		<form>
			<swiper :current="subjectIndex" class="swiper-box" @change="SwiperChange" :style="{'height':swiperHeight}">
				<swiper-item v-for="(subject,index) in subjectList">
					
					<view v-if="index-subjectIndex>=-1&&index-subjectIndex<=1">
										
					<view class="cu-bar bg-white solid-bottom">
						<view class="action text-black">
							<text class="cuIcon-title text-red"></text>{{subject.title}}
						</view>
					</view>
					<view>

						<radio-group class="block"  @change="RadioboxChange" v-if="subject.type===1||subject.type===2">
							<view class="cu-form-group" v-for="option in subject.optionList">
								<radio :value="option.id"></radio>
								<view class="title text-black">{{option.id}}.{{option.content}}</view>
							</view>
						</radio-group>

						<checkbox-group class="block"  @change="CheckboxChange" v-else-if="subject.type===3">
							<view class="cu-form-group" v-for="option in subject.optionList">
								<checkbox :value="option.id" :class="subject.userAnswer.indexOf(option.id) > -1?'checked':''" :checked="subject.userAnswer.indexOf(option.id) > -1?true:false"></checkbox>
								<view class="title  text-black">{{option.id}}.{{option.content}}</view>
							</view>
						</checkbox-group>

						<view v-else-if="subject.type===4">
							<view class="cu-form-group solid-bottom">
								<view class="title  text-black">
									答：
								</view>
								<input placeholder="文本输入框" name="input" @blur="textInput" ></input>
							</view>
						</view>

						<view v-else-if="subject.type===5">
							<view class="cu-bar cu-bar-title bg-white margin-top">
								<view class="action  text-black">
									答：
								</view>
							</view>
							<view class="cu-form-group solid margin">
								<textarea maxlength="-1"  @blur="textInput" placeholder="多行文本输入框"></textarea>
							</view>
						</view>

					</view>

					<view v-show="subject.showAnswer" class="margin-top solid-top">
						<view class="cu-bar">
							<view class="action  text-grey">
								<text>正确答案：</text>
								<text class="solid-bottom  padding-left text-green">{{subject.answer}}</text>
							</view>
						</view>
						<view class="cu-bar cu-bar-title">
							<view class="action  text-grey">
								<text>解析：</text>
							</view>
						</view>
						<view class="text-content padding  text-grey">
							{{subject.explain}}
						</view>
					</view>

					</view>
				</swiper-item>
			</swiper>
		</form>
		<view id="foot-box" class="cu-bar tabbar bg-white shadow foot">
			<view class="action" @click="MoveSubject(-1)">
				<view class="cuIcon-cu-image">
					<text class="lg cuIcon-back text-gray"></text>
				</view>
				<view class="text-gray">上一题</view>
			</view>
			<view class="action" @click="MoveSubject(1)">
				<view class="cuIcon-cu-image">
					<text class="lg text-gray cuIcon-right"></text>
				</view>
				<view class="text-gray">下一题</view>
			</view>

			<view class="action" @click="FavorSubject">
				<view class="cuIcon-cu-image">
					<text class="lg cuIcon-favor" :class="[userFavor?'text-red':'text-gray']"></text>
				</view>
				<view  :class="[userFavor?'text-red':'text-gray']">收藏</view>
			</view>

			<view class="action" @click="ShowAnswerChange">
				<view class="cuIcon-cu-image">
					<text class="lg text-gray cuIcon-question"></text>
				</view>
				<view class="text-gray">解答</view>
			</view>
			<view class="action" @tap="showErrorModal"  data-target="modalError">
				<view class="cuIcon-cu-image">
					<text class="lg text-gray cuIcon-warn"></text>
				</view>
				<view class="text-gray">纠错</view>
			</view>

		</view>

	</view>
</template>

<script>
	export default {
		data() {
			return {
				userFavor:false,//是否已收藏
				currentType: 0, //当前题型
				subjectIndex: 0,//跳转索引
				autoShowAnswer: false,//答错是否显答案
				autoRadioNext:true,//判断题、单项题，自动移下一题
				swiperHeight: '800px',//
				title: '初中二年级2019期中考券',
				subjectList:[
					{"title":"水是液体？","type":1,"optionList":[{"id":"A","content":"对"},{"id":"B","content":"错"}],"answer":"A","userAnswer":"","userFavor":false,"explain":"难到是固体不成？"},
					{"title":"电流分有？","type":2,"optionList":[{"id":"A","content":"直流"},{"id":"B","content":"交流"},{"id":"C","content":"直流和交流"}],"answer":"C","userAnswer":"","userFavor":false,"explain":"科技学依据"},
					{"title":"酸菜鱼的味道？","type":3,"optionList":[{"id":"A","content":"咸味"},{"id":"B","content":"辣味"},{"id":"C","content":"甜味"},{"id":"D","content":"酸味"}],"answer":"A,B,D","userAnswer":"","userFavor":false,"explain":"你怎么想都行，要的就是这个味，答案只能选A,B,D"},
					{"title":"床前（____）光，疑是地上霜。","type":4,"optionList":[{"id":"","content":""}],"answer":"明月","userAnswer":"","userFavor":false,"explain":"问答题没有选项，无法做答，且不参与计分"},
					{"title":"什么美国要限制华为？","type":5,"optionList":[{"id":"","content":""}],"answer":"","userAnswer":"","userFavor":false,"explain":"问答题没有选项，无法做答，且不参与计分"},
										
					{"title":"水是液体？","type":1,"optionList":[{"id":"A","content":"对"},{"id":"B","content":"错"}],"answer":"A","userAnswer":"","userFavor":false,"explain":"难到是固体不成？"},
					{"title":"电流分有？","type":2,"optionList":[{"id":"A","content":"直流"},{"id":"B","content":"交流"},{"id":"C","content":"直流和交流"}],"answer":"C","userAnswer":"","userFavor":false,"explain":"科技学依据"},
					{"title":"酸菜鱼的味道？","type":3,"optionList":[{"id":"A","content":"咸味"},{"id":"B","content":"辣味"},{"id":"C","content":"甜味"},{"id":"D","content":"酸味"}],"answer":"A,B,D","userAnswer":"","userFavor":false,"explain":"你怎么想都行，要的就是这个味，答案只能选A,B,D"},
					{"title":"床前（____）光，疑是地上霜。","type":4,"optionList":[{"id":"","content":""}],"answer":"明月","userAnswer":"","userFavor":false,"explain":"问答题没有选项，无法做答，且不参与计分"},
					{"title":"什么美国要限制华为？","type":5,"optionList":[{"id":"","content":""}],"answer":"","userAnswer":"","userFavor":false,"explain":"问答题没有选项，无法做答，且不参与计分"},
					
					{"title":"水是液体？","type":1,"optionList":[{"id":"A","content":"对"},{"id":"B","content":"错"}],"answer":"A","userAnswer":"","userFavor":false,"explain":"难到是固体不成？"},
					{"title":"电流分有？","type":2,"optionList":[{"id":"A","content":"直流"},{"id":"B","content":"交流"},{"id":"C","content":"直流和交流"}],"answer":"C","userAnswer":"","userFavor":false,"explain":"科技学依据"},
					{"title":"酸菜鱼的味道？","type":3,"optionList":[{"id":"A","content":"咸味"},{"id":"B","content":"辣味"},{"id":"C","content":"甜味"},{"id":"D","content":"酸味"}],"answer":"A,B,D","userAnswer":"","userFavor":false,"explain":"你怎么想都行，要的就是这个味，答案只能选A,B,D"},
					{"title":"床前（____）光，疑是地上霜。","type":4,"optionList":[{"id":"","content":""}],"answer":"明月","userAnswer":"","userFavor":false,"explain":"问答题没有选项，无法做答，且不参与计分"},
					{"title":"什么美国要限制华为？","type":5,"optionList":[{"id":"","content":""}],"answer":"","userAnswer":"","userFavor":false,"explain":"问答题没有选项，无法做答，且不参与计分"},
					
					{"title":"水是液体？","type":1,"optionList":[{"id":"A","content":"对"},{"id":"B","content":"错"}],"answer":"A","userAnswer":"","userFavor":false,"explain":"难到是固体不成？"},
					{"title":"电流分有？","type":2,"optionList":[{"id":"A","content":"直流"},{"id":"B","content":"交流"},{"id":"C","content":"直流和交流"}],"answer":"C","userAnswer":"","userFavor":false,"explain":"科技学依据"},
					{"title":"酸菜鱼的味道？","type":3,"optionList":[{"id":"A","content":"咸味"},{"id":"B","content":"辣味"},{"id":"C","content":"甜味"},{"id":"D","content":"酸味"}],"answer":"A,B,D","userAnswer":"","userFavor":false,"explain":"你怎么想都行，要的就是这个味，答案只能选A,B,D"},
					{"title":"床前（____）光，疑是地上霜。","type":4,"optionList":[{"id":"","content":""}],"answer":"明月","userAnswer":"","userFavor":false,"explain":"问答题没有选项，无法做答，且不参与计分"},
					{"title":"什么美国要限制华为？","type":5,"optionList":[{"id":"","content":""}],"answer":"","userAnswer":"","userFavor":false,"explain":"问答题没有选项，无法做答，且不参与计分"},
					
					{"title":"水是液体？","type":1,"optionList":[{"id":"A","content":"对"},{"id":"B","content":"错"}],"answer":"A","userAnswer":"","userFavor":false,"explain":"难到是固体不成？"},
					{"title":"电流分有？","type":2,"optionList":[{"id":"A","content":"直流"},{"id":"B","content":"交流"},{"id":"C","content":"直流和交流"}],"answer":"C","userAnswer":"","userFavor":false,"explain":"科技学依据"},
					{"title":"酸菜鱼的味道？","type":3,"optionList":[{"id":"A","content":"咸味"},{"id":"B","content":"辣味"},{"id":"C","content":"甜味"},{"id":"D","content":"酸味"}],"answer":"A,B,D","userAnswer":"","userFavor":false,"explain":"你怎么想都行，要的就是这个味，答案只能选A,B,D"},
					{"title":"床前（____）光，疑是地上霜。","type":4,"optionList":[{"id":"","content":""}],"answer":"明月","userAnswer":"","userFavor":false,"explain":"问答题没有选项，无法做答，且不参与计分"},
					{"title":"什么美国要限制华为？","type":5,"optionList":[{"id":"","content":""}],"answer":"","userAnswer":"","userFavor":false,"explain":"问答题没有选项，无法做答，且不参与计分"},
					
					{"title":"水是液体？","type":1,"optionList":[{"id":"A","content":"对"},{"id":"B","content":"错"}],"answer":"A","userAnswer":"","userFavor":false,"explain":"难到是固体不成？"},
					{"title":"电流分有？","type":2,"optionList":[{"id":"A","content":"直流"},{"id":"B","content":"交流"},{"id":"C","content":"直流和交流"}],"answer":"C","userAnswer":"","userFavor":false,"explain":"科技学依据"},
					{"title":"酸菜鱼的味道？","type":3,"optionList":[{"id":"A","content":"咸味"},{"id":"B","content":"辣味"},{"id":"C","content":"甜味"},{"id":"D","content":"酸味"}],"answer":"A,B,D","userAnswer":"","userFavor":false,"explain":"你怎么想都行，要的就是这个味，答案只能选A,B,D"},
					{"title":"床前（____）光，疑是地上霜。","type":4,"optionList":[{"id":"","content":""}],"answer":"明月","userAnswer":"","userFavor":false,"explain":"问答题没有选项，无法做答，且不参与计分"},
					{"title":"什么美国要限制华为？","type":5,"optionList":[{"id":"","content":""}],"answer":"","userAnswer":"","userFavor":false,"explain":"问答题没有选项，无法做答，且不参与计分"},
					
					{"title":"水是液体？","type":1,"optionList":[{"id":"A","content":"对"},{"id":"B","content":"错"}],"answer":"A","userAnswer":"","userFavor":false,"explain":"难到是固体不成？"},
					{"title":"电流分有？","type":2,"optionList":[{"id":"A","content":"直流"},{"id":"B","content":"交流"},{"id":"C","content":"直流和交流"}],"answer":"C","userAnswer":"","userFavor":false,"explain":"科技学依据"},
					{"title":"酸菜鱼的味道？","type":3,"optionList":[{"id":"A","content":"咸味"},{"id":"B","content":"辣味"},{"id":"C","content":"甜味"},{"id":"D","content":"酸味"}],"answer":"A,B,D","userAnswer":"","userFavor":false,"explain":"你怎么想都行，要的就是这个味，答案只能选A,B,D"},
					{"title":"床前（____）光，疑是地上霜。","type":4,"optionList":[{"id":"","content":""}],"answer":"明月","userAnswer":"","userFavor":false,"explain":"问答题没有选项，无法做答，且不参与计分"},
					{"title":"什么美国要限制华为？","type":5,"optionList":[{"id":"","content":""}],"answer":"","userAnswer":"","userFavor":false,"explain":"问答题没有选项，无法做答，且不参与计分"},
					
					{"title":"水是液体？","type":1,"optionList":[{"id":"A","content":"对"},{"id":"B","content":"错"}],"answer":"A","userAnswer":"","userFavor":false,"explain":"难到是固体不成？"},
					{"title":"电流分有？","type":2,"optionList":[{"id":"A","content":"直流"},{"id":"B","content":"交流"},{"id":"C","content":"直流和交流"}],"answer":"C","userAnswer":"","userFavor":false,"explain":"科技学依据"},
					{"title":"酸菜鱼的味道？","type":3,"optionList":[{"id":"A","content":"咸味"},{"id":"B","content":"辣味"},{"id":"C","content":"甜味"},{"id":"D","content":"酸味"}],"answer":"A,B,D","userAnswer":"","userFavor":false,"explain":"你怎么想都行，要的就是这个味，答案只能选A,B,D"},
					{"title":"床前（____）光，疑是地上霜。","type":4,"optionList":[{"id":"","content":""}],"answer":"明月","userAnswer":"","userFavor":false,"explain":"问答题没有选项，无法做答，且不参与计分"},
					{"title":"什么美国要限制华为？","type":5,"optionList":[{"id":"","content":""}],"answer":"","userAnswer":"","userFavor":false,"explain":"问答题没有选项，无法做答，且不参与计分"},
					
					{"title":"水是液体？","type":1,"optionList":[{"id":"A","content":"对"},{"id":"B","content":"错"}],"answer":"A","userAnswer":"","userFavor":false,"explain":"难到是固体不成？"},
					{"title":"电流分有？","type":2,"optionList":[{"id":"A","content":"直流"},{"id":"B","content":"交流"},{"id":"C","content":"直流和交流"}],"answer":"C","userAnswer":"","userFavor":false,"explain":"科技学依据"},
					{"title":"酸菜鱼的味道？","type":3,"optionList":[{"id":"A","content":"咸味"},{"id":"B","content":"辣味"},{"id":"C","content":"甜味"},{"id":"D","content":"酸味"}],"answer":"A,B,D","userAnswer":"","userFavor":false,"explain":"你怎么想都行，要的就是这个味，答案只能选A,B,D"},
					{"title":"床前（____）光，疑是地上霜。","type":4,"optionList":[{"id":"","content":""}],"answer":"明月","userAnswer":"","userFavor":false,"explain":"问答题没有选项，无法做答，且不参与计分"},
					{"title":"什么美国要限制华为？","type":5,"optionList":[{"id":"","content":""}],"answer":"","userAnswer":"","userFavor":false,"explain":"问答题没有选项，无法做答，且不参与计分"},
					
					{"title":"水是液体？","type":1,"optionList":[{"id":"A","content":"对"},{"id":"B","content":"错"}],"answer":"A","userAnswer":"","userFavor":false,"explain":"难到是固体不成？"},
					{"title":"电流分有？","type":2,"optionList":[{"id":"A","content":"直流"},{"id":"B","content":"交流"},{"id":"C","content":"直流和交流"}],"answer":"C","userAnswer":"","userFavor":false,"explain":"科技学依据"},
					{"title":"酸菜鱼的味道？","type":3,"optionList":[{"id":"A","content":"咸味"},{"id":"B","content":"辣味"},{"id":"C","content":"甜味"},{"id":"D","content":"酸味"}],"answer":"A,B,D","userAnswer":"","userFavor":false,"explain":"你怎么想都行，要的就是这个味，答案只能选A,B,D"},
					{"title":"床前（____）光，疑是地上霜。","type":4,"optionList":[{"id":"","content":""}],"answer":"明月","userAnswer":"","userFavor":false,"explain":"问答题没有选项，无法做答，且不参与计分"},
					{"title":"什么美国要限制华为？","type":5,"optionList":[{"id":"","content":""}],"answer":"","userAnswer":"","userFavor":false,"explain":"问答题没有选项，无法做答，且不参与计分"},
					
					{"title":"水是液体？","type":1,"optionList":[{"id":"A","content":"对"},{"id":"B","content":"错"}],"answer":"A","userAnswer":"","userFavor":false,"explain":"难到是固体不成？"},
					{"title":"电流分有？","type":2,"optionList":[{"id":"A","content":"直流"},{"id":"B","content":"交流"},{"id":"C","content":"直流和交流"}],"answer":"C","userAnswer":"","userFavor":false,"explain":"科技学依据"},
					{"title":"酸菜鱼的味道？","type":3,"optionList":[{"id":"A","content":"咸味"},{"id":"B","content":"辣味"},{"id":"C","content":"甜味"},{"id":"D","content":"酸味"}],"answer":"A,B,D","userAnswer":"","userFavor":false,"explain":"你怎么想都行，要的就是这个味，答案只能选A,B,D"},
					{"title":"床前（____）光，疑是地上霜。","type":4,"optionList":[{"id":"","content":""}],"answer":"明月","userAnswer":"","userFavor":false,"explain":"问答题没有选项，无法做答，且不参与计分"},
					{"title":"什么美国要限制华为？","type":5,"optionList":[{"id":"","content":""}],"answer":"","userAnswer":"","userFavor":false,"explain":"问答题没有选项，无法做答，且不参与计分"},
					
					{"title":"水是液体？","type":1,"optionList":[{"id":"A","content":"对"},{"id":"B","content":"错"}],"answer":"A","userAnswer":"","userFavor":false,"explain":"难到是固体不成？"},
					{"title":"电流分有？","type":2,"optionList":[{"id":"A","content":"直流"},{"id":"B","content":"交流"},{"id":"C","content":"直流和交流"}],"answer":"C","userAnswer":"","userFavor":false,"explain":"科技学依据"},
					{"title":"酸菜鱼的味道？","type":3,"optionList":[{"id":"A","content":"咸味"},{"id":"B","content":"辣味"},{"id":"C","content":"甜味"},{"id":"D","content":"酸味"}],"answer":"A,B,D","userAnswer":"","userFavor":false,"explain":"你怎么想都行，要的就是这个味，答案只能选A,B,D"},
					{"title":"床前（____）光，疑是地上霜。","type":4,"optionList":[{"id":"","content":""}],"answer":"明月","userAnswer":"","userFavor":false,"explain":"问答题没有选项，无法做答，且不参与计分"},
					{"title":"什么美国要限制华为？","type":5,"optionList":[{"id":"","content":""}],"answer":"","userAnswer":"","userFavor":false,"explain":"问答题没有选项，无法做答，且不参与计分"},
					
					{"title":"水是液体？","type":1,"optionList":[{"id":"A","content":"对"},{"id":"B","content":"错"}],"answer":"A","userAnswer":"","userFavor":false,"explain":"难到是固体不成？"},
					{"title":"电流分有？","type":2,"optionList":[{"id":"A","content":"直流"},{"id":"B","content":"交流"},{"id":"C","content":"直流和交流"}],"answer":"C","userAnswer":"","userFavor":false,"explain":"科技学依据"},
					{"title":"酸菜鱼的味道？","type":3,"optionList":[{"id":"A","content":"咸味"},{"id":"B","content":"辣味"},{"id":"C","content":"甜味"},{"id":"D","content":"酸味"}],"answer":"A,B,D","userAnswer":"","userFavor":false,"explain":"你怎么想都行，要的就是这个味，答案只能选A,B,D"},
					{"title":"床前（____）光，疑是地上霜。","type":4,"optionList":[{"id":"","content":""}],"answer":"明月","userAnswer":"","userFavor":false,"explain":"问答题没有选项，无法做答，且不参与计分"},
					{"title":"什么美国要限制华为？","type":5,"optionList":[{"id":"","content":""}],"answer":"","userAnswer":"","userFavor":false,"explain":"问答题没有选项，无法做答，且不参与计分"},
					
					{"title":"水是液体？","type":1,"optionList":[{"id":"A","content":"对"},{"id":"B","content":"错"}],"answer":"A","userAnswer":"","userFavor":false,"explain":"难到是固体不成？"},
					{"title":"电流分有？","type":2,"optionList":[{"id":"A","content":"直流"},{"id":"B","content":"交流"},{"id":"C","content":"直流和交流"}],"answer":"C","userAnswer":"","userFavor":false,"explain":"科技学依据"},
					{"title":"酸菜鱼的味道？","type":3,"optionList":[{"id":"A","content":"咸味"},{"id":"B","content":"辣味"},{"id":"C","content":"甜味"},{"id":"D","content":"酸味"}],"answer":"A,B,D","userAnswer":"","userFavor":false,"explain":"你怎么想都行，要的就是这个味，答案只能选A,B,D"},
					{"title":"床前（____）光，疑是地上霜。","type":4,"optionList":[{"id":"","content":""}],"answer":"明月","userAnswer":"","userFavor":false,"explain":"问答题没有选项，无法做答，且不参与计分"},
					{"title":"什么美国要限制华为？","type":5,"optionList":[{"id":"","content":""}],"answer":"","userAnswer":"","userFavor":false,"explain":"问答题没有选项，无法做答，且不参与计分"},
					
					{"title":"水是液体？","type":1,"optionList":[{"id":"A","content":"对"},{"id":"B","content":"错"}],"answer":"A","userAnswer":"","userFavor":false,"explain":"难到是固体不成？"},
					{"title":"电流分有？","type":2,"optionList":[{"id":"A","content":"直流"},{"id":"B","content":"交流"},{"id":"C","content":"直流和交流"}],"answer":"C","userAnswer":"","userFavor":false,"explain":"科技学依据"},
					{"title":"酸菜鱼的味道？","type":3,"optionList":[{"id":"A","content":"咸味"},{"id":"B","content":"辣味"},{"id":"C","content":"甜味"},{"id":"D","content":"酸味"}],"answer":"A,B,D","userAnswer":"","userFavor":false,"explain":"你怎么想都行，要的就是这个味，答案只能选A,B,D"},
					{"title":"床前（____）光，疑是地上霜。","type":4,"optionList":[{"id":"","content":""}],"answer":"明月","userAnswer":"","userFavor":false,"explain":"问答题没有选项，无法做答，且不参与计分"},
					{"title":"什么美国要限制华为？","type":5,"optionList":[{"id":"","content":""}],"answer":"","userAnswer":"","userFavor":false,"explain":"问答题没有选项，无法做答，且不参与计分"},
					
					{"title":"水是液体？","type":1,"optionList":[{"id":"A","content":"对"},{"id":"B","content":"错"}],"answer":"A","userAnswer":"","userFavor":false,"explain":"难到是固体不成？"},
					{"title":"电流分有？","type":2,"optionList":[{"id":"A","content":"直流"},{"id":"B","content":"交流"},{"id":"C","content":"直流和交流"}],"answer":"C","userAnswer":"","userFavor":false,"explain":"科技学依据"},
					{"title":"酸菜鱼的味道？","type":3,"optionList":[{"id":"A","content":"咸味"},{"id":"B","content":"辣味"},{"id":"C","content":"甜味"},{"id":"D","content":"酸味"}],"answer":"A,B,D","userAnswer":"","userFavor":false,"explain":"你怎么想都行，要的就是这个味，答案只能选A,B,D"},
					{"title":"床前（____）光，疑是地上霜。","type":4,"optionList":[{"id":"","content":""}],"answer":"明月","userAnswer":"","userFavor":false,"explain":"问答题没有选项，无法做答，且不参与计分"},
					{"title":"什么美国要限制华为？","type":5,"optionList":[{"id":"","content":""}],"answer":"","userAnswer":"","userFavor":false,"explain":"问答题没有选项，无法做答，且不参与计分"},
					
					{"title":"水是液体？","type":1,"optionList":[{"id":"A","content":"对"},{"id":"B","content":"错"}],"answer":"A","userAnswer":"","userFavor":false,"explain":"难到是固体不成？"},
					{"title":"电流分有？","type":2,"optionList":[{"id":"A","content":"直流"},{"id":"B","content":"交流"},{"id":"C","content":"直流和交流"}],"answer":"C","userAnswer":"","userFavor":false,"explain":"科技学依据"},
					{"title":"酸菜鱼的味道？","type":3,"optionList":[{"id":"A","content":"咸味"},{"id":"B","content":"辣味"},{"id":"C","content":"甜味"},{"id":"D","content":"酸味"}],"answer":"A,B,D","userAnswer":"","userFavor":false,"explain":"你怎么想都行，要的就是这个味，答案只能选A,B,D"},
					{"title":"床前（____）光，疑是地上霜。","type":4,"optionList":[{"id":"","content":""}],"answer":"明月","userAnswer":"","userFavor":false,"explain":"问答题没有选项，无法做答，且不参与计分"},					
					
					{"title":"水是液体？","type":1,"optionList":[{"id":"A","content":"对"},{"id":"B","content":"错"}],"answer":"A","userAnswer":"","userFavor":false,"explain":"难到是固体不成？"},
					{"title":"电流分有？","type":2,"optionList":[{"id":"A","content":"直流"},{"id":"B","content":"交流"},{"id":"C","content":"直流和交流"}],"answer":"C","userAnswer":"","userFavor":false,"explain":"科技学依据"},
					{"title":"酸菜鱼的味道？","type":3,"optionList":[{"id":"A","content":"咸味"},{"id":"B","content":"辣味"},{"id":"C","content":"甜味"},{"id":"D","content":"酸味"}],"answer":"A,B,D","userAnswer":"","userFavor":false,"explain":"你怎么想都行，要的就是这个味，答案只能选A,B,D"},
					{"title":"床前（____）光，疑是地上霜。","type":4,"optionList":[{"id":"","content":""}],"answer":"明月","userAnswer":"","userFavor":false,"explain":"问答题没有选项，无法做答，且不参与计分"},
					
					{"title":"水是液体？","type":1,"optionList":[{"id":"A","content":"对"},{"id":"B","content":"错"}],"answer":"A","userAnswer":"","userFavor":false,"explain":"难到是固体不成？"},
					{"title":"电流分有？","type":2,"optionList":[{"id":"A","content":"直流"},{"id":"B","content":"交流"},{"id":"C","content":"直流和交流"}],"answer":"C","userAnswer":"","userFavor":false,"explain":"科技学依据"},
					{"title":"酸菜鱼的味道？","type":3,"optionList":[{"id":"A","content":"咸味"},{"id":"B","content":"辣味"},{"id":"C","content":"甜味"},{"id":"D","content":"酸味"}],"answer":"A,B,D","userAnswer":"","userFavor":false,"explain":"你怎么想都行，要的就是这个味，答案只能选A,B,D"},
					{"title":"床前（____）光，疑是地上霜。","type":4,"optionList":[{"id":"","content":""}],"answer":"明月","userAnswer":"","userFavor":false,"explain":"问答题没有选项，无法做答，且不参与计分"},
					
					{"title":"水是液体？","type":1,"optionList":[{"id":"A","content":"对"},{"id":"B","content":"错"}],"answer":"A","userAnswer":"","userFavor":false,"explain":"难到是固体不成？"},
					{"title":"电流分有？","type":2,"optionList":[{"id":"A","content":"直流"},{"id":"B","content":"交流"},{"id":"C","content":"直流和交流"}],"answer":"C","userAnswer":"","userFavor":false,"explain":"科技学依据"},
					{"title":"酸菜鱼的味道？","type":3,"optionList":[{"id":"A","content":"咸味"},{"id":"B","content":"辣味"},{"id":"C","content":"甜味"},{"id":"D","content":"酸味"}],"answer":"A,B,D","userAnswer":"","userFavor":false,"explain":"你怎么想都行，要的就是这个味，答案只能选A,B,D"},
					{"title":"床前（____）光，疑是地上霜。","type":4,"optionList":[{"id":"","content":""}],"answer":"明月","userAnswer":"","userFavor":false,"explain":"问答题没有选项，无法做答，且不参与计分"},
					
					{"title":"水是液体？","type":1,"optionList":[{"id":"A","content":"对"},{"id":"B","content":"错"}],"answer":"A","userAnswer":"","userFavor":false,"explain":"难到是固体不成？"},
					{"title":"电流分有？","type":2,"optionList":[{"id":"A","content":"直流"},{"id":"B","content":"交流"},{"id":"C","content":"直流和交流"}],"answer":"C","userAnswer":"","userFavor":false,"explain":"科技学依据"},
					{"title":"酸菜鱼的味道？","type":3,"optionList":[{"id":"A","content":"咸味"},{"id":"B","content":"辣味"},{"id":"C","content":"甜味"},{"id":"D","content":"酸味"}],"answer":"A,B,D","userAnswer":"","userFavor":false,"explain":"你怎么想都行，要的就是这个味，答案只能选A,B,D"},
					{"title":"床前（____）光，疑是地上霜。","type":4,"optionList":[{"id":"","content":""}],"answer":"明月","userAnswer":"","userFavor":false,"explain":"问答题没有选项，无法做答，且不参与计分"},
					
					{"title":"水是液体？","type":1,"optionList":[{"id":"A","content":"对"},{"id":"B","content":"错"}],"answer":"A","userAnswer":"","userFavor":false,"explain":"难到是固体不成？"},
					{"title":"电流分有？","type":2,"optionList":[{"id":"A","content":"直流"},{"id":"B","content":"交流"},{"id":"C","content":"直流和交流"}],"answer":"C","userAnswer":"","userFavor":false,"explain":"科技学依据"},
					{"title":"酸菜鱼的味道？","type":3,"optionList":[{"id":"A","content":"咸味"},{"id":"B","content":"辣味"},{"id":"C","content":"甜味"},{"id":"D","content":"酸味"}],"answer":"A,B,D","userAnswer":"","userFavor":false,"explain":"你怎么想都行，要的就是这个味，答案只能选A,B,D"},
					{"title":"床前（____）光，疑是地上霜。","type":4,"optionList":[{"id":"","content":""}],"answer":"明月","userAnswer":"","userFavor":false,"explain":"问答题没有选项，无法做答，且不参与计分"},
					
					{"title":"水是液体？","type":1,"optionList":[{"id":"A","content":"对"},{"id":"B","content":"错"}],"answer":"A","userAnswer":"","userFavor":false,"explain":"难到是固体不成？"},
					{"title":"电流分有？","type":2,"optionList":[{"id":"A","content":"直流"},{"id":"B","content":"交流"},{"id":"C","content":"直流和交流"}],"answer":"C","userAnswer":"","userFavor":false,"explain":"科技学依据"},
					{"title":"酸菜鱼的味道？","type":3,"optionList":[{"id":"A","content":"咸味"},{"id":"B","content":"辣味"},{"id":"C","content":"甜味"},{"id":"D","content":"酸味"}],"answer":"A,B,D","userAnswer":"","userFavor":false,"explain":"你怎么想都行，要的就是这个味，答案只能选A,B,D"},
					{"title":"床前（____）光，疑是地上霜。","type":4,"optionList":[{"id":"","content":""}],"answer":"明月","userAnswer":"","userFavor":false,"explain":"问答题没有选项，无法做答，且不参与计分"},
					
					{"title":"水是液体？","type":1,"optionList":[{"id":"A","content":"对"},{"id":"B","content":"错"}],"answer":"A","userAnswer":"","userFavor":false,"explain":"难到是固体不成？"},
					{"title":"电流分有？","type":2,"optionList":[{"id":"A","content":"直流"},{"id":"B","content":"交流"},{"id":"C","content":"直流和交流"}],"answer":"C","userAnswer":"","userFavor":false,"explain":"科技学依据"},
					{"title":"酸菜鱼的味道？","type":3,"optionList":[{"id":"A","content":"咸味"},{"id":"B","content":"辣味"},{"id":"C","content":"甜味"},{"id":"D","content":"酸味"}],"answer":"A,B,D","userAnswer":"","userFavor":false,"explain":"你怎么想都行，要的就是这个味，答案只能选A,B,D"},
					{"title":"床前（____）光，疑是地上霜。","type":4,"optionList":[{"id":"","content":""}],"answer":"明月","userAnswer":"","userFavor":false,"explain":"问答题没有选项，无法做答，且不参与计分"}
					
					
				   ],
				modalCard: null ,//显示答题卡
				modalError:null , //纠错卡
				errorList:['题目不完整','答案不正确','含有错别字','图片不存在','解析不完整','其他错误']
			}
		},
		onReady() {

			var tempHeight = 800;
			var _me = this;
			uni.getSystemInfo({
				//获取手机屏幕高度信息，让swiper的高度和手机屏幕一样高                
				success: function(res) {
					// console.log(res.model);                    
					// console.log(res.pixelRatio);                    
					// console.log(res.windowWidth);                    
					// console.log(res.windowHeight);
					// //这里是手机屏幕高度                    
					// console.log(res.language);                    
					// console.log(res.version);                    
					// console.log(res.platform);                    
					tempHeight = res.windowHeight;
					console.log("屏幕可用高度 " + tempHeight);

					uni.createSelectorQuery().select("#top-box").fields({
						size: true,
						scrollOffset: true
					}, (data) => {
						tempHeight -= data.height;
						console.log("减掉顶部后的高度 " + tempHeight);

						uni.createSelectorQuery().select("#foot-box").fields({
							size: true,
							scrollOffset: true
						}, (data) => {
							tempHeight -= data.height;
							console.log("减掉底部后的高度 " + tempHeight);
							_me.swiperHeight = tempHeight + 'px';
							console.log("滑屏最后高度 " + _me.swiperHeight);
						}).exec();

					}).exec();
				}
			});

		},
		onLoad() {
			
			this.currentType = this.subjectList[0].type;
			uni.setNavigationBarTitle({
				title: this.title
			});			
			
			//添加用户显示答案字段
			for (var i = 0; i < this.subjectList.length; i++) {		
				this.$set(this.subjectList[i],"showAnswer",false);				
			}
			
		},
		methods: {
			showCardModal: function(e) {
				this.modalCard = e.currentTarget.dataset.target
			},
			hideCardModal: function(e) {
				this.modalCard = null
			},
			showErrorModal: function(e) {
				this.modalError = e.currentTarget.dataset.target
			},
			hideErrorModal: function(e) {
				this.modalError = null
			},
			SwiperChange: function(e) { //滑动事件
			
				let index = e.target.current;
				if (index != undefined) {
					this.subjectIndex = index;
					this.currentType = this.subjectList[index].type;
					this.userFavor = this.subjectList[index].userFavor;
				}
								
			},
			
			RadioboxChange : function(e) { //单选选中
			
				var items = this.subjectList[this.subjectIndex].optionList;
				var values = e.detail.value;
				this.subjectList[this.subjectIndex].userAnswer = values;
				if(this.autoRadioNext && this.subjectIndex < this.subjectList.length - 1){
					this.subjectIndex += 1;						
					};
				
			},
			CheckboxChange: function(e) { //复选选中

				var items = this.subjectList[this.subjectIndex].optionList;
				var values = e.detail.value;
				this.subjectList[this.subjectIndex].userAnswer = "";
				for (var i = 0, lenI = items.length; i < lenI; ++i) {
					for (var j = 0, lenJ = values.length; j < lenJ; ++j) {
						if (items[i].id == values[j]) {

							this.subjectList[this.subjectIndex].userAnswer += items[i].id;
							break
						}
					}
				}
			},
			textInput : function(e) { //填空题
			
				this.subjectList[this.subjectIndex].userAnswer = e.detail.value;
				
			},			
			ShowAnswerChange: function(e) { //显示答案
			
				if(this.subjectList[this.subjectIndex].showAnswer)
				{
					this.subjectList[this.subjectIndex].showAnswer=false;					
				}
				else{
					
					this.subjectList[this.subjectIndex].showAnswer=true;
				}				
			},
			
			FavorSubject: function(e) { //收藏题
			
				if(this.userFavor)
				{
					this.userFavor=false;
					this.subjectList[this.subjectIndex].userFavor=false;					
				}
				else{
					
					this.userFavor=true;
					this.subjectList[this.subjectIndex].userFavor=true;	
				}				
			},
			
			MoveSubject: function(e) { //上一题、下一题

				if (e === -1 && this.subjectIndex != 0) {
					this.subjectIndex -= 1;
				}
				if (e === 1 && this.subjectIndex < this.subjectList.length - 1) {
					this.subjectIndex += 1;
				}
			},
			
			AppointedSubject: function(e) { //题卡指定
				
					this.modalCard = null;
					this.subjectIndex = e;									
			},			
			
			SubmitError: function(e) { //提交纠错
				
					this.modalError = null;														
			}
			
		}
	}
</script>

<style>
	@import "../../colorui/animation.css";
	page {
		background-color: #FFFFFF;
	}

	.cu-form-group {
		justify-content: flex-start
	}

	.cu-form-group .title {
		padding-left: 30upx;
		padding-right: 0upx;
	}

	.cu-form-group+.cu-form-group {
		border-top: none;
	}

	.cu-bar-title {
		min-height: 50upx;
	}
	
	.cu-list.menu>.cu-item-error{justify-content: flex-start;}
</style>
