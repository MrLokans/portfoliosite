var gulp = require('gulp');
var cleanCSS = require('gulp-clean-css');
var concat = require('gulp-concat');
var inject = require('gulp-inject');
var minify = require('gulp-minify');
var less = require('gulp-less');
var ngConstant = require('gulp-ng-constant');
var rename = require('gulp-rename');
var watch = require('gulp-watch');
var webserver = require('gulp-webserver');
var debug = require('gulp-debug');
var gulpFilter = require('gulp-filter');

var del = require('del');

var mainBowerFiles = require('gulp-main-bower-files');
var bowerFiles = require('main-bower-files');

PATHS = {
  BUILD: 'build',
  THIRDPARTY: 'build/3rdparty'
}

// Cleans up build folder before the build start
gulp.task('clean:build', function(){
    return del.sync(PATHS.BUILD);
});
 

// Runs the development webserver
gulp.task('webserver', function() {
  gulp.src('build/')
    .pipe(webserver({
      port: 8090,
      livereload: true,
      directoryListing: false,
      open: true
    }));
});


gulp.task('concat:angular-dev',
          ['copy:assets', 'config:dev'],
          function(){
    return gulp
        .src(['js/app/app.js', 'build/app.constants.js', 'js/app/*.js', 'js/app/**/*.js'])
        .pipe(concat('angular.app.js'))
        .pipe(gulp.dest('build/'));
});

gulp.task('concat:angular-prod',
          ['copy:assets', 'config:prod'],
          function(){
    return gulp
        .src(['js/app/app.js', 'build/app.constants.js', 'js/app/*.js', 'js/app/**/*.js'])
        .pipe(concat('angular.app.js'))
        .pipe(minify({
            ext:{
              source: '.js',
              min: '.min.js'
            }
          }))
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


// --------------- FILE COPYING -----------------
gulp.task('copy:bower-components', function(){
    // return gulp.src(['./bower_components/**/*'])
    //     .pipe(gulp.dest('build/bower_components/'));
});

gulp.task('copy:angular', function(){
    // Copies angular js scripts
    return gulp.src(['js/app/**/*'])
        .pipe(gulp.dest('build/js/app/'));
});

gulp.task('copy:js', function(){
    // Copies custom javascript
    return gulp.src(['js/*.js'])
        .pipe(gulp.dest('build/js/'));
});

gulp.task('copy:vendor-css', function(){
    return gulp.src(['js/vendor/**/*.css'])
        .pipe(gulp.dest('build/js/vendor/'));
});

gulp.task('copy:vendor-js', function(){
    return gulp.src(['js/vendor/**/*.js'])
        .pipe(gulp.dest('build/js/vendor/'));
});

gulp.task('copy:styles', function(){
    return gulp.src(['./css/*.css'])
        .pipe(gulp.dest('build/css'));
});

gulp.task('copy:images', function(){
    return gulp.src(['./img/**/*.png',
              './img/**/*/jpg',
              './img/**/*.svg'])
        .pipe(gulp.dest('build/img'));
});

gulp.task('copy:assets',
          ['copy:js', 'copy:vendor-js', 'copy:vendor-css', 
           'copy:styles', 'copy:images'],
          function(){});


gulp.task('copy:3rdparty-dev', function(){
  return gulp.src(bowerFiles())
    .pipe(debug({title: 'copy:3rdparty'}))
    .pipe(gulp.dest('build/3rdparty'));
});

gulp.task('clean:3rdparty-dev', ['rename-analytics-script:dev', 'less:3rdparty'], function(){
  var filter = ['build/3rdparty/**/*.*',
                '!build/3rdparty/**/*.js',
                '!build/3rdparty/**/*.css',
                'build/3rdparty/angulartics-ga.js']
  return del.sync(filter)
});

// --------------- FILE INJECTION ---------------
gulp.task('inject:dev', ['concat:angular-dev', 'clean:3rdparty-dev'], function(){
    // Inject bower dependencies
    return gulp.src('./index.html')
        // We need specific order for jquery, bootstrap and angular
        .pipe(inject(gulp.src(['build/3rdparty/jquery.js',
                               'build/3rdparty/bootstrap.js',
                               'build/3rdparty/angular.js'], {read: false}),
                     {name: 'bower-first'}))
        // Bower components
        .pipe(inject(gulp.src(['build/3rdparty/*.*',
                               '!build/3rdparty/**/jquery.js',
                               '!build/3rdparty/**/bootstrap.js',
                               '!build/3rdparty/**/angular.js'], {read: false}),
                      {name: 'bower'}))
        .pipe(inject(gulp.src('build/angular.app.js', {read: false}), {name: 'app'}))
        .pipe(debug({title: 'inject:dev'}))
        .pipe(gulp.dest('build'));
});

gulp.task('inject:prod',
          ['clean:3rdparty', 'concat:angular-prod'],
          function(){
    // First level dependencies
    firstLevel = gulp.src(['build/3rdparty/**/jquery.min.js',
                           'build/3rdparty/**/bootstrap.min.js',
                           'build/3rdparty/**/angular.min.js'], {read: false})
    // Inject bower dependencies
    thirdpartySrc = gulp.src(['build/3rdparty/**/*.min.css',
                              'build/3rdparty/**/*.min.js',
                              '!build/3rdparty/**/jquery.min.js',
                              '!build/3rdparty/**/bootstrap.min.js',
                              '!build/3rdparty/**/angular.min.js'],
                               {read: false});
    appPath = gulp.src(['build/angular.app.min.js'], {read: false})

    return gulp.src('./index.html')
      .pipe(inject(firstLevel, {name: 'bower-first'}))
      .pipe(inject(thirdpartySrc, {name: 'bower'}))
      .pipe(inject(appPath, {name: 'app'}))
      .pipe(gulp.dest('build'));
});



gulp.task('copy:3rdparty', function(){
    return gulp.src('./bower.json')
        .pipe(mainBowerFiles())
        .pipe(gulp.dest(PATHS.THIRDPARTY));
})


gulp.task('less:3rdparty', ['copy:3rdparty'], function(){
  return gulp.src(['build/3rdparty/**/*.less'])
    .pipe(less())
    .pipe(debug({title: 'LESS'}))
    .pipe(gulp.dest(PATHS.THIRDPARTY))
})

// We need to rename analytics script in order for it
// not to be blocked by ublock
gulp.task('rename-analytics-script:prod', ['copy:3rdparty'], function(){
  return gulp
    .src('build/3rdparty/**/angulartics-ga.js')
    .pipe(rename(function(path){
      path.basename = 'my-analysis-script'
    }))
    .pipe(gulp.dest(PATHS.THIRDPARTY))
});

// We need to rename analytics script in order for it
// not to be blocked by ublock
gulp.task('rename-analytics-script:dev', ['copy:3rdparty-dev'], function(){
  return gulp
    .src('build/3rdparty/**/angulartics-ga.js')
    .pipe(rename(function(path){
      path.basename = 'my-analysis-script'
    }))
    .pipe(gulp.dest(PATHS.THIRDPARTY))
});

gulp.task('minify:3rdparty-js', ['rename-analytics-script:prod'], function(){
    var filesToMinify = ['build/3rdparty/**/*.js',
                         '!build/3rdparty/**/*.min.js']
    var filterMinified = gulpFilter(['**/*.min.js', '!**/*.min.min.*']);
    return gulp.src(filesToMinify)
        .pipe(minify({
            ext:{
              source: '.js',
              min: '.min.js'
            }
          }))
        .pipe(filterMinified)
        .pipe(debug({title: 'Minify'}))
        .pipe(gulp.dest(PATHS.THIRDPARTY));
});

gulp.task('minify:3rdparty-css', ['copy:3rdparty'], function(){
    var filesToMinify = ['build/3rdparty/**/*.css',
                         '!build/3rdparty/**/*.min.css']
    var filterMinified = gulpFilter(['**/*.min.css', '!**/*.min.min.*']);
    return gulp.src(filesToMinify)
        .pipe(cleanCSS())
        .pipe(filterMinified)
        .pipe(debug({title: 'Minify CSS'}))
        .pipe(gulp.dest(PATHS.THIRDPARTY));
});

// Cleans up non-minified files
// and renamed files
gulp.task('clean:3rdparty', ['minify:3rdparty-js', 'minify:3rdparty-css'], function(){
  removedPaths = [
    'build/3rdparty/**/*.*',
    '!build/3rdparty/**/*.min.js',
    '!build/3rdparty/**/*.min.css',
    'build/3rdparty/**/angulartics-ga.min.js'
  ]
  del.sync(removedPaths);
})

gulp.task('build-dev',
          ['config:dev', 'inject:dev']);

gulp.task('build-prod',
          ['config:prod', 'inject:prod'],
          function(){});

gulp.task('default',
          ['clean:build', 'build-dev'],
          function(){
    gulp.watch(['js/**', 'index.html', 'css/**'], function(event){
        gulp.run('copy:assets');
        gulp.run('build-dev');
    });
});

gulp.task('prod',
          ['clean:build', 'build-prod'],
          function(){});
