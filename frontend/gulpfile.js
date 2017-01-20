var gulp = require('gulp');
var clean = require('gulp-clean');
var cleanCSS = require('gulp-clean-css');
var concat = require('gulp-concat');
var inject = require('gulp-inject');
var minify = require('gulp-minify');
var ngConstant = require('gulp-ng-constant');
var rename = require('gulp-rename');
var watch = require('gulp-watch');
var webserver = require('gulp-webserver');
var debug = require('gulp-debug');

var bowerFiles = require('main-bower-files');


gulp.task('clean:build', function(){
    return gulp.src('build/**/*.*', {read: false}).pipe(clean());
});
 

gulp.task('webserver', function() {
  gulp.src('build/')
    .pipe(webserver({
      port: 8090,
      livereload: true,
      directoryListing: false,
      open: true
    }));
});


gulp.task('concat:angular', function(){
    gulp.src(['js/app/app.js', 'build/app.constants.js', 'js/app/*.js', 'js/app/**/*.js'])
        .pipe(debug())
        .pipe(concat('angular.app.js'))
        .pipe(gulp.dest('build/'));
});


gulp.task('config:dev', function(){
    return gulp.src('js/configs/dev.json')
          .pipe(ngConstant({
                "name": "andersblog.constants",
                "deps": [],
                "wrap": false,
                "wrapHeader": "(function(){",
                "wrapFooter": "});"
              }))
          .pipe(rename('app.constants.js'))
          .pipe(gulp.dest('build/'));
});

gulp.task('config:prod', function(){
    return gulp.src('js/configs/prod.json')
          .pipe(ngConstant({
                "name": "andersblog.constants",
                "deps": [],
                "wrap": false,
                "wrapHeader": "(function(){",
                "wrapFooter": "});"
              }))
          .pipe(rename('app.constants.js'))
          .pipe(gulp.dest('build/'))
});

gulp.task('copy:bower-components', function(){
    gulp.src(['./bower_components/**/*'])
        .pipe(gulp.dest('build/bower_components/'));
});

gulp.task('copy:angular', function(){
    // Copies angular js scripts
    gulp.src(['js/app/**/*'])
        .pipe(gulp.dest('build/js/app/'));
});

gulp.task('copy:js', function(){
    // Copies custom javascript
    gulp.src(['js/*.js'])
        .pipe(gulp.dest('build/js/'));
});

gulp.task('copy:vendor-css', function(){
    gulp.src(['js/vendor/**/*.css'])
        .pipe(gulp.dest('build/js/vendor/'));
});

gulp.task('copy:vendor-js', function(){
    gulp.src(['js/vendor/**/*.js'])
        .pipe(gulp.dest('build/js/vendor/'));
});

gulp.task('copy:styles', function(){
    gulp.src(['./css/*.css'])
        .pipe(gulp.dest('build/css'));
});

gulp.task('copy:images', function(){
    gulp.src(['./img/**/*.png',
              './img/**/*/jpg',
              './img/**/*.svg'])
        .pipe(gulp.dest('build/img'));
});

gulp.task('inject:bower', function(){
    // Inject bower dependencies
    gulp.src('./index.html')
        .pipe(inject(gulp.src(bowerFiles(), {read: false}), {name: 'bower'}))
        .pipe(gulp.dest('build'));
});

gulp.task('build-dev', ['config:dev'], function(){
    gulp.run('concat:angular');
    gulp.run('inject:bower');
});

gulp.task('build-prod', ['config:prod'], function(){
    gulp.run('concat:angular');
    gulp.run('inject:bower');
});

gulp.task('copy:assets', ['copy:bower-components',
                          'copy:js', 'copy:vendor-js', 'copy:vendor-css', 
                          'copy:styles',
                          'copy:images'], function(){

});

gulp.task('default', ['clean:build'], function(){
    gulp.run('copy:assets');
    gulp.run('build-dev');
    gulp.run('webserver');
    gulp.watch(['js/**', 'index.html', 'css/**'], function(event){
        gulp.run('copy:assets');
        gulp.run('build-dev');
    });
});

gulp.task('prod', ['clean:build'], function(){
    gulp.run('copy:assets');
    gulp.run('build-prod');
});
