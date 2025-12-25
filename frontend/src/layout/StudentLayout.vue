<template>
  <div>
    <el-menu mode="horizontal" router>
      <el-menu-item index="/student">个人信息</el-menu-item>
      <el-menu-item index="/student/project">提交项目</el-menu-item>
      <el-menu-item index="/student/achievements">成果</el-menu-item>
      <el-menu-item index="/student/scores">成绩</el-menu-item>
      <el-menu-item index="/student/ai">AI 推荐</el-menu-item>
    </el-menu>
    <router-view />
  </div>
</template>
