<template>
  <div>
    <el-menu mode="horizontal" router>
      <el-menu-item index="/teacher">项目评分</el-menu-item>
      <el-menu-item index="/teacher/ai">AI 问答</el-menu-item>
    </el-menu>
    <router-view />
  </div>
</template>
