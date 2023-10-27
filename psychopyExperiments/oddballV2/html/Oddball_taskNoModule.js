/********************* 
 * Oddball_Task Test *
 *********************/

// init psychoJS:
var psychoJS = new PsychoJS({
  debug: true
});

// open window:
psychoJS.openWindow({
  fullscr: true,
  color: new util.Color([0, 0, 0]),
  units: 'use prefs'
});

// store info about the experiment session:
let expName = 'Oddball_task';  // from the Builder filename that created this script
let expInfo = {'participant': '', 'session': '001'};

// schedule the experiment:
psychoJS.schedule(psychoJS.gui.DlgFromDict({
  dictionary: expInfo,
  title: expName
}));

const flowScheduler = new Scheduler(psychoJS);
const dialogCancelScheduler = new Scheduler(psychoJS);
psychoJS.scheduleCondition(function() { return (psychoJS.gui.dialogComponent.button === 'OK'); }, flowScheduler, dialogCancelScheduler);

// flowScheduler gets run if the participants presses OK
flowScheduler.add(updateInfo); // add timeStamp
flowScheduler.add(experimentInit);
flowScheduler.add(InstructionsRoutineBegin);
flowScheduler.add(InstructionsRoutineEachFrame);
flowScheduler.add(InstructionsRoutineEnd);
const trialsLoopScheduler = new Scheduler(psychoJS);
flowScheduler.add(trialsLoopBegin, trialsLoopScheduler);
flowScheduler.add(trialsLoopScheduler);
flowScheduler.add(trialsLoopEnd);
flowScheduler.add(Instructions_2RoutineBegin);
flowScheduler.add(Instructions_2RoutineEachFrame);
flowScheduler.add(Instructions_2RoutineEnd);
const trials_2LoopScheduler = new Scheduler(psychoJS);
flowScheduler.add(trials_2LoopBegin, trials_2LoopScheduler);
flowScheduler.add(trials_2LoopScheduler);
flowScheduler.add(trials_2LoopEnd);
flowScheduler.add(EndRoutineBegin);
flowScheduler.add(EndRoutineEachFrame);
flowScheduler.add(EndRoutineEnd);
flowScheduler.add(quitPsychoJS, '', true);

// quit if user presses Cancel in dialog box:
dialogCancelScheduler.add(quitPsychoJS, '', false);

psychoJS.start({configURL: 'config.json', expInfo: expInfo});

var frameDur;
function updateInfo() {
  expInfo['date'] = util.MonotonicClock.getDateStr();  // add a simple timestamp
  expInfo['expName'] = expName;
  expInfo['psychopyVersion'] = '3.0.2';

  // store frame rate of monitor if we can measure it successfully
  expInfo['frameRate'] = psychoJS.window.getActualFrameRate();
  if (typeof expInfo['frameRate'] !== 'undefined')
    frameDur = 1.0/Math.round(expInfo['frameRate']);
  else
    frameDur = 1.0/60.0; // couldn't get a reliable measure so guess

  // add info from the URL:
  util.addInfoFromUrl(expInfo);
  
  return Scheduler.Event.NEXT;
}

var InstructionsClock;
var instruction;
var TrialClock;
var fixation_point;
var left_circle;
var right_circle;
var left_square;
var right_square;
var FeedbackClock;
var text;
var Instructions_2Clock;
var text_2;
var EndClock;
var text_3;
var globalClock;
var routineTimer;
function experimentInit() {
  // Initialize components for Routine "Instructions"
  InstructionsClock = new util.Clock();
  instruction = new visual.TextStim({
    win: psychoJS.window,
    name: 'instruction',
    text: 'In this task you will be required to categorise the presented stimuli based on shape. Press z for circle and m for square. Ignore which side the shape apears on. This is a practice trail and feedback will be provided. Press space to continue.',
    font: 'Arial',
    pos: [0, 0], height: 0.1,  wrapWidth: undefined, ori: 0,
    color: new util.Color('white'),  opacity: 1,
    depth: 0.0 
  });
  
  // Initialize components for Routine "Trial"
  TrialClock = new util.Clock();
  fixation_point = new visual.TextStim({
    win: psychoJS.window,
    name: 'fixation_point',
    text: '+',
    font: 'Arial',
    pos: [0, 0], height: 0.1,  wrapWidth: undefined, ori: 0,
    color: new util.Color('white'),  opacity: 1,
    depth: 0.0 
  });
  
  left_circle = new visual.Rect ({
    win: psychoJS.window, name: 'left_circle',
    units: psychoJS.window.units,
    width: [0.25, 0.25][0], height: [0.25, 0.25][1],
    ori: 0, pos: [(- 0.25), 0],
    lineWidth: 1, lineColor: new util.Color([1.0, 1.0, 1.0]),
    fillColor: new util.Color([1.0, 1.0, 1.0]),
    opacity: 1, depth: -1.0, interpolate: true,
  });
  
  right_circle = new visual.Rect ({
    win: psychoJS.window, name: 'right_circle',
    units: psychoJS.window.units,
    width: [0.25, 0.25][0], height: [0.25, 0.25][1],
    ori: 0, pos: [0.25, 0],
    lineWidth: 1, lineColor: new util.Color([1.0, 1.0, 1.0]),
    fillColor: new util.Color([1.0, 1.0, 1.0]),
    opacity: 1, depth: -1.0, interpolate: true,
  });
  
  left_square = new visual.Rect ({
    win: psychoJS.window, name: 'left_square',
    units: psychoJS.window.units,
    width: [0.25, 0.25][0], height: [0.25, 0.25][1],
    ori: 0, pos: [(- 0.25), 0],
    lineWidth: 1, lineColor: new util.Color([1.0, 1.0, 1.0]),
    fillColor: new util.Color([1.0, 1.0, 1.0]),
    opacity: 1, depth: -1.0, interpolate: true,
  });
  
  right_square = new visual.Rect ({
    win: psychoJS.window, name: 'right_square',
    units: psychoJS.window.units,
    width: [0.25, 0.25][0], height: [0.25, 0.25][1],
    ori: 0, pos: [0.25, 0],
    lineWidth: 1, lineColor: new util.Color([1.0, 1.0, 1.0]),
    fillColor: new util.Color([1.0, 1.0, 1.0]),
    opacity: 1, depth: -1.0, interpolate: true,
  });
  
  // Initialize components for Routine "Feedback"
  FeedbackClock = new util.Clock();
  
  text = new visual.TextStim({
    win: psychoJS.window,
    name: 'text',
    text: 'default text',
    font: 'Arial',
    pos: [0, 0], height: 0.1,  wrapWidth: undefined, ori: 0,
    color: new util.Color('white'),  opacity: 1,
    depth: -1.0 
  });
  
  // Initialize components for Routine "Instructions_2"
  Instructions_2Clock = new util.Clock();
  text_2 = new visual.TextStim({
    win: psychoJS.window,
    name: 'text_2',
    text: 'This is the end of practice trials and start of experimental trials. Feedback will not be provided anymore. Press space to continue.',
    font: 'Arial',
    pos: [0, 0], height: 0.1,  wrapWidth: undefined, ori: 0,
    color: new util.Color('white'),  opacity: 1,
    depth: 0.0 
  });
  
  // Initialize components for Routine "Trial"
  TrialClock = new util.Clock();
  fixation_point = new visual.TextStim({
    win: psychoJS.window,
    name: 'fixation_point',
    text: '+',
    font: 'Arial',
    pos: [0, 0], height: 0.1,  wrapWidth: undefined, ori: 0,
    color: new util.Color('white'),  opacity: 1,
    depth: 0.0 
  });
  
  left_circle = new visual.Rect ({
    win: psychoJS.window, name: 'left_circle',
    units: psychoJS.window.units,
    width: [0.25, 0.25][0], height: [0.25, 0.25][1],
    ori: 0, pos: [(- 0.25), 0],
    lineWidth: 1, lineColor: new util.Color([1.0, 1.0, 1.0]),
    fillColor: new util.Color([1.0, 1.0, 1.0]),
    opacity: 1, depth: -1.0, interpolate: true,
  });
  
  right_circle = new visual.Rect ({
    win: psychoJS.window, name: 'right_circle',
    units: psychoJS.window.units,
    width: [0.25, 0.25][0], height: [0.25, 0.25][1],
    ori: 0, pos: [0.25, 0],
    lineWidth: 1, lineColor: new util.Color([1.0, 1.0, 1.0]),
    fillColor: new util.Color([1.0, 1.0, 1.0]),
    opacity: 1, depth: -1.0, interpolate: true,
  });
  
  left_square = new visual.Rect ({
    win: psychoJS.window, name: 'left_square',
    units: psychoJS.window.units,
    width: [0.25, 0.25][0], height: [0.25, 0.25][1],
    ori: 0, pos: [(- 0.25), 0],
    lineWidth: 1, lineColor: new util.Color([1.0, 1.0, 1.0]),
    fillColor: new util.Color([1.0, 1.0, 1.0]),
    opacity: 1, depth: -1.0, interpolate: true,
  });
  
  right_square = new visual.Rect ({
    win: psychoJS.window, name: 'right_square',
    units: psychoJS.window.units,
    width: [0.25, 0.25][0], height: [0.25, 0.25][1],
    ori: 0, pos: [0.25, 0],
    lineWidth: 1, lineColor: new util.Color([1.0, 1.0, 1.0]),
    fillColor: new util.Color([1.0, 1.0, 1.0]),
    opacity: 1, depth: -1.0, interpolate: true,
  });
  
  // Initialize components for Routine "End"
  EndClock = new util.Clock();
  text_3 = new visual.TextStim({
    win: psychoJS.window,
    name: 'text_3',
    text: 'This is the end of the experiment.\n\nThank you for your time.',
    font: 'Arial',
    pos: [0, 0], height: 0.1,  wrapWidth: undefined, ori: 0,
    color: new util.Color('white'),  opacity: 1,
    depth: 0.0 
  });
  
  // Create some handy timers
  globalClock = new util.Clock();  // to track the time since experiment started
  routineTimer = new util.CountdownTimer();  // to track time remaining of each (non-slip) routine
  
  return Scheduler.Event.NEXT;
}

var t;
var frameN;
var key_resp_1;
var InstructionsComponents;
function InstructionsRoutineBegin() {
  //------Prepare to start Routine 'Instructions'-------
  t = 0;
  InstructionsClock.reset(); // clock
  frameN = -1;
  // update component parameters for each repeat
  key_resp_1 = new core.BuilderKeyResponse(psychoJS);
  // keep track of which components have finished
  InstructionsComponents = [];
  InstructionsComponents.push(instruction);
  InstructionsComponents.push(key_resp_1);
  
  for (const thisComponent of InstructionsComponents)
    if ('status' in thisComponent)
      thisComponent.status = PsychoJS.Status.NOT_STARTED;
  
  return Scheduler.Event.NEXT;
}

var continueRoutine;
function InstructionsRoutineEachFrame() {
  //------Loop for each frame of Routine 'Instructions'-------
  let continueRoutine = true; // until we're told otherwise
  // get current time
  t = InstructionsClock.getTime();
  frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
  // update/draw components on each frame
  
  // *instruction* updates
  if (t >= 0.0 && instruction.status === PsychoJS.Status.NOT_STARTED) {
    // keep track of start time/frame for later
    instruction.tStart = t;  // (not accounting for frame time here)
    instruction.frameNStart = frameN;  // exact frame index
    instruction.setAutoDraw(true);
  }

  
  // *key_resp_1* updates
  if (t >= 0.0 && key_resp_1.status === PsychoJS.Status.NOT_STARTED) {
    // keep track of start time/frame for later
    key_resp_1.tStart = t;  // (not accounting for frame time here)
    key_resp_1.frameNStart = frameN;  // exact frame index
    key_resp_1.status = PsychoJS.Status.STARTED;
    // keyboard checking is just starting
    psychoJS.window.callOnFlip(function() { key_resp_1.clock.reset(); }); // t = 0 on screen flip
    psychoJS.eventManager.clearEvents({eventType:'keyboard'});
  }

  if (key_resp_1.status === PsychoJS.Status.STARTED) {
    let theseKeys = psychoJS.eventManager.getKeys({keyList:['space']});
    
    // check for quit:
    if (theseKeys.indexOf('escape') > -1) {
        psychoJS.experiment.experimentEnded = true;
    }
    if (theseKeys.length > 0) {  // at least one key was pressed
      key_resp_1.keys = theseKeys[theseKeys.length-1];  // just the last key pressed
      key_resp_1.rt = key_resp_1.clock.getTime();
      // a response ends the routine
      continueRoutine = false;
    }
  }
  // check for quit (typically the Esc key)
  if (psychoJS.experiment.experimentEnded || psychoJS.eventManager.getKeys({keyList:['escape']}).length > 0) {
    return psychoJS.quit('The [Escape] key was pressed. Goodbye!', false);
  }
  
  // check if the Routine should terminate
  if (!continueRoutine) {  // a component has requested a forced-end of Routine
    return Scheduler.Event.NEXT;
  }
  
  continueRoutine = false;// reverts to True if at least one component still running
  for (const thisComponent of InstructionsComponents)
    if ('status' in thisComponent && thisComponent.status !== PsychoJS.Status.FINISHED) {
      continueRoutine = true;
      break;
    }
  
  // check for quit (the Esc key)
  if (psychoJS.experiment.experimentEnded || psychoJS.eventManager.getKeys({keyList:['escape']}).length > 0) {
    return quitPsychoJS('The [Escape] key was pressed. Goodbye!', false);
  }
  
  // refresh the screen if continuing
  if (continueRoutine) {
    return Scheduler.Event.FLIP_REPEAT;
  }
  else {
    return Scheduler.Event.NEXT;
  }
}


function InstructionsRoutineEnd() {
  //------Ending Routine 'Instructions'-------
  for (const thisComponent of InstructionsComponents) {
    if (typeof thisComponent.setAutoDraw === 'function') {
      thisComponent.setAutoDraw(false);
    }
  }
  
  // check responses
  if (['', [], undefined].indexOf(key_resp_1.keys) >= 0) {    // No response was made
      key_resp_1.keys = undefined;
  }
  
  psychoJS.experiment.addData('key_resp_1.keys', key_resp_1.keys);
  if (typeof key_resp_1.keys !== 'undefined') {  // we had a response
      psychoJS.experiment.addData('key_resp_1.rt', key_resp_1.rt);
      routineTimer.reset();
      }
  
  // the Routine "Instructions" was not non-slip safe, so reset the non-slip timer
  routineTimer.reset();
  
  return Scheduler.Event.NEXT;
}

var trials;
function trialsLoopBegin(thisScheduler) {
  // set up handler to look after randomisation of conditions etc
  trials = new TrialHandler({
    psychoJS,
    nReps: 5, method: TrialHandler.Method.RANDOM,
    extraInfo: expInfo, originPath: undefined,
    trialList: 'trials.xlsx',
    seed: undefined, name: 'trials'});
  psychoJS.experiment.addLoop(trials); // add the loop to the experiment

  // Schedule all the trials in the trialList:
  for (const thisTrial of trials) {
    thisScheduler.add(importConditions(trials));
    thisScheduler.add(TrialRoutineBegin);
    thisScheduler.add(TrialRoutineEachFrame);
    thisScheduler.add(TrialRoutineEnd);
    thisScheduler.add(FeedbackRoutineBegin);
    thisScheduler.add(FeedbackRoutineEachFrame);
    thisScheduler.add(FeedbackRoutineEnd);
    thisScheduler.add(endLoopIteration(thisTrial));
  }

  return Scheduler.Event.NEXT;
}


function trialsLoopEnd() {
  psychoJS.experiment.removeLoop(trials);

  return Scheduler.Event.NEXT;
}

var trials_2;
function trials_2LoopBegin(thisScheduler) {
  // set up handler to look after randomisation of conditions etc
  trials_2 = new TrialHandler({
    psychoJS,
    nReps: 5, method: TrialHandler.Method.RANDOM,
    extraInfo: expInfo, originPath: undefined,
    trialList: 'trials.xlsx',
    seed: undefined, name: 'trials_2'});
  psychoJS.experiment.addLoop(trials_2); // add the loop to the experiment

  // Schedule all the trials in the trialList:
  for (const thisTrial_2 of trials_2) {
    thisScheduler.add(importConditions(trials_2));
    thisScheduler.add(TrialRoutineBegin);
    thisScheduler.add(TrialRoutineEachFrame);
    thisScheduler.add(TrialRoutineEnd);
    thisScheduler.add(endLoopIteration(thisTrial_2));
  }

  return Scheduler.Event.NEXT;
}


function trials_2LoopEnd() {
  psychoJS.experiment.removeLoop(trials_2);

  return Scheduler.Event.NEXT;
}

var key_resp_2;
var TrialComponents;
function TrialRoutineBegin() {
  //------Prepare to start Routine 'Trial'-------
  t = 0;
  TrialClock.reset(); // clock
  frameN = -1;
  // update component parameters for each repeat
  left_circle.setOpacity(circle_left);
  right_circle.setOpacity(circle_right);
  left_square.setOpacity(square_left);
  right_square.setOpacity(square_right);
  key_resp_2 = new core.BuilderKeyResponse(psychoJS);
  // keep track of which components have finished
  TrialComponents = [];
  TrialComponents.push(fixation_point);
  TrialComponents.push(left_circle);
  TrialComponents.push(right_circle);
  TrialComponents.push(left_square);
  TrialComponents.push(right_square);
  TrialComponents.push(key_resp_2);
  
  for (const thisComponent of TrialComponents)
    if ('status' in thisComponent)
      thisComponent.status = PsychoJS.Status.NOT_STARTED;
  
  return Scheduler.Event.NEXT;
}


function TrialRoutineEachFrame() {
  //------Loop for each frame of Routine 'Trial'-------
  let continueRoutine = true; // until we're told otherwise
  // get current time
  t = TrialClock.getTime();
  frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
  // update/draw components on each frame
  
  // *fixation_point* updates
  if (t >= 0.0 && fixation_point.status === PsychoJS.Status.NOT_STARTED) {
    // keep track of start time/frame for later
    fixation_point.tStart = t;  // (not accounting for frame time here)
    fixation_point.frameNStart = frameN;  // exact frame index
    fixation_point.setAutoDraw(true);
  }

  
  // *left_circle* updates
  if (t >= 0.0 && left_circle.status === PsychoJS.Status.NOT_STARTED) {
    // keep track of start time/frame for later
    left_circle.tStart = t;  // (not accounting for frame time here)
    left_circle.frameNStart = frameN;  // exact frame index
    left_circle.setAutoDraw(true);
  }

  
  // *right_circle* updates
  if (t >= 0.0 && right_circle.status === PsychoJS.Status.NOT_STARTED) {
    // keep track of start time/frame for later
    right_circle.tStart = t;  // (not accounting for frame time here)
    right_circle.frameNStart = frameN;  // exact frame index
    right_circle.setAutoDraw(true);
  }

  
  // *left_square* updates
  if (t >= 0.0 && left_square.status === PsychoJS.Status.NOT_STARTED) {
    // keep track of start time/frame for later
    left_square.tStart = t;  // (not accounting for frame time here)
    left_square.frameNStart = frameN;  // exact frame index
    left_square.setAutoDraw(true);
  }

  
  // *right_square* updates
  if (t >= 0.0 && right_square.status === PsychoJS.Status.NOT_STARTED) {
    // keep track of start time/frame for later
    right_square.tStart = t;  // (not accounting for frame time here)
    right_square.frameNStart = frameN;  // exact frame index
    right_square.setAutoDraw(true);
  }

  
  // *key_resp_2* updates
  if (t >= 0.0 && key_resp_2.status === PsychoJS.Status.NOT_STARTED) {
    // keep track of start time/frame for later
    key_resp_2.tStart = t;  // (not accounting for frame time here)
    key_resp_2.frameNStart = frameN;  // exact frame index
    key_resp_2.status = PsychoJS.Status.STARTED;
    // keyboard checking is just starting
    psychoJS.window.callOnFlip(function() { key_resp_2.clock.reset(); }); // t = 0 on screen flip
    psychoJS.eventManager.clearEvents({eventType:'keyboard'});
  }

  if (key_resp_2.status === PsychoJS.Status.STARTED) {
    let theseKeys = psychoJS.eventManager.getKeys({keyList:['z', 'm']});
    
    // check for quit:
    if (theseKeys.indexOf('escape') > -1) {
        psychoJS.experiment.experimentEnded = true;
    }
    if (theseKeys.length > 0) {  // at least one key was pressed
      key_resp_2.keys = theseKeys[theseKeys.length-1];  // just the last key pressed
      key_resp_2.rt = key_resp_2.clock.getTime();
      // was this 'correct'?
      if (key_resp_2.keys == corrAns) {
          key_resp_2.corr = 1;
      } else {
          key_resp_2.corr = 0;
      }
      // a response ends the routine
      continueRoutine = false;
    }
  }
  // check for quit (typically the Esc key)
  if (psychoJS.experiment.experimentEnded || psychoJS.eventManager.getKeys({keyList:['escape']}).length > 0) {
    return psychoJS.quit('The [Escape] key was pressed. Goodbye!', false);
  }
  
  // check if the Routine should terminate
  if (!continueRoutine) {  // a component has requested a forced-end of Routine
    return Scheduler.Event.NEXT;
  }
  
  continueRoutine = false;// reverts to True if at least one component still running
  for (const thisComponent of TrialComponents)
    if ('status' in thisComponent && thisComponent.status !== PsychoJS.Status.FINISHED) {
      continueRoutine = true;
      break;
    }
  
  // check for quit (the Esc key)
  if (psychoJS.experiment.experimentEnded || psychoJS.eventManager.getKeys({keyList:['escape']}).length > 0) {
    return quitPsychoJS('The [Escape] key was pressed. Goodbye!', false);
  }
  
  // refresh the screen if continuing
  if (continueRoutine) {
    return Scheduler.Event.FLIP_REPEAT;
  }
  else {
    return Scheduler.Event.NEXT;
  }
}


function TrialRoutineEnd() {
  //------Ending Routine 'Trial'-------
  for (const thisComponent of TrialComponents) {
    if (typeof thisComponent.setAutoDraw === 'function') {
      thisComponent.setAutoDraw(false);
    }
  }
  
  // check responses
  if (['', [], undefined].indexOf(key_resp_2.keys) >= 0) {    // No response was made
      key_resp_2.keys = undefined;
  }
  
  // was no response the correct answer?!
  if (key_resp_2.keys == undefined) {
    if (psychoJS.str(corrAns).toLowerCase() == 'none') {
       key_resp_2.corr = 1  // correct non-response
    } else {
       key_resp_2.corr = 0  // failed to respond (incorrectly)
    }
  }
  // store data for thisExp (ExperimentHandler)
  psychoJS.experiment.addData('key_resp_2.keys', key_resp_2.keys);
  psychoJS.experiment.addData('key_resp_2.corr', key_resp_2.corr);
  if (typeof key_resp_2.keys !== 'undefined') {  // we had a response
      psychoJS.experiment.addData('key_resp_2.rt', key_resp_2.rt);
      routineTimer.reset();
      }
  
  // the Routine "Trial" was not non-slip safe, so reset the non-slip timer
  routineTimer.reset();
  
  return Scheduler.Event.NEXT;
}

var FeedbackComponents;
function FeedbackRoutineBegin() {
  //------Prepare to start Routine 'Feedback'-------
  t = 0;
  FeedbackClock.reset(); // clock
  frameN = -1;
  routineTimer.add(1.000000);
  // update component parameters for each repeat
  
  text.setText(msg);
  // keep track of which components have finished
  FeedbackComponents = [];
  FeedbackComponents.push(text);
  
  for (const thisComponent of FeedbackComponents)
    if ('status' in thisComponent)
      thisComponent.status = PsychoJS.Status.NOT_STARTED;
  
  return Scheduler.Event.NEXT;
}

var frameRemains;
function FeedbackRoutineEachFrame() {
  //------Loop for each frame of Routine 'Feedback'-------
  let continueRoutine = true; // until we're told otherwise
  // get current time
  t = FeedbackClock.getTime();
  frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
  // update/draw components on each frame
  
  
  // *text* updates
  if (t >= 0.0 && text.status === PsychoJS.Status.NOT_STARTED) {
    // keep track of start time/frame for later
    text.tStart = t;  // (not accounting for frame time here)
    text.frameNStart = frameN;  // exact frame index
    text.setAutoDraw(true);
  }

  frameRemains = 0.0 + 1.0 - psychoJS.window.monitorFramePeriod * 0.75;  // most of one frame period left
  if (text.status === PsychoJS.Status.STARTED && t >= frameRemains) {
    text.setAutoDraw(false);
  }
  // check for quit (typically the Esc key)
  if (psychoJS.experiment.experimentEnded || psychoJS.eventManager.getKeys({keyList:['escape']}).length > 0) {
    return psychoJS.quit('The [Escape] key was pressed. Goodbye!', false);
  }
  
  // check if the Routine should terminate
  if (!continueRoutine) {  // a component has requested a forced-end of Routine
    return Scheduler.Event.NEXT;
  }
  
  continueRoutine = false;// reverts to True if at least one component still running
  for (const thisComponent of FeedbackComponents)
    if ('status' in thisComponent && thisComponent.status !== PsychoJS.Status.FINISHED) {
      continueRoutine = true;
      break;
    }
  
  // check for quit (the Esc key)
  if (psychoJS.experiment.experimentEnded || psychoJS.eventManager.getKeys({keyList:['escape']}).length > 0) {
    return quitPsychoJS('The [Escape] key was pressed. Goodbye!', false);
  }
  
  // refresh the screen if continuing
  if (continueRoutine && routineTimer.getTime() > 0) {
    return Scheduler.Event.FLIP_REPEAT;
  }
  else {
    return Scheduler.Event.NEXT;
  }
}


function FeedbackRoutineEnd() {
  //------Ending Routine 'Feedback'-------
  for (const thisComponent of FeedbackComponents) {
    if (typeof thisComponent.setAutoDraw === 'function') {
      thisComponent.setAutoDraw(false);
    }
  }
  
  return Scheduler.Event.NEXT;
}

var key_resp_3;
var Instructions_2Components;
function Instructions_2RoutineBegin() {
  //------Prepare to start Routine 'Instructions_2'-------
  t = 0;
  Instructions_2Clock.reset(); // clock
  frameN = -1;
  // update component parameters for each repeat
  key_resp_3 = new core.BuilderKeyResponse(psychoJS);
  // keep track of which components have finished
  Instructions_2Components = [];
  Instructions_2Components.push(text_2);
  Instructions_2Components.push(key_resp_3);
  
  for (const thisComponent of Instructions_2Components)
    if ('status' in thisComponent)
      thisComponent.status = PsychoJS.Status.NOT_STARTED;
  
  return Scheduler.Event.NEXT;
}


function Instructions_2RoutineEachFrame() {
  //------Loop for each frame of Routine 'Instructions_2'-------
  let continueRoutine = true; // until we're told otherwise
  // get current time
  t = Instructions_2Clock.getTime();
  frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
  // update/draw components on each frame
  
  // *text_2* updates
  if (t >= 0.0 && text_2.status === PsychoJS.Status.NOT_STARTED) {
    // keep track of start time/frame for later
    text_2.tStart = t;  // (not accounting for frame time here)
    text_2.frameNStart = frameN;  // exact frame index
    text_2.setAutoDraw(true);
  }

  
  // *key_resp_3* updates
  if (t >= 0.0 && key_resp_3.status === PsychoJS.Status.NOT_STARTED) {
    // keep track of start time/frame for later
    key_resp_3.tStart = t;  // (not accounting for frame time here)
    key_resp_3.frameNStart = frameN;  // exact frame index
    key_resp_3.status = PsychoJS.Status.STARTED;
    // keyboard checking is just starting
    psychoJS.window.callOnFlip(function() { key_resp_3.clock.reset(); }); // t = 0 on screen flip
    psychoJS.eventManager.clearEvents({eventType:'keyboard'});
  }

  if (key_resp_3.status === PsychoJS.Status.STARTED) {
    let theseKeys = psychoJS.eventManager.getKeys({keyList:['space']});
    
    // check for quit:
    if (theseKeys.indexOf('escape') > -1) {
        psychoJS.experiment.experimentEnded = true;
    }
    if (theseKeys.length > 0) {  // at least one key was pressed
      key_resp_3.keys = theseKeys[theseKeys.length-1];  // just the last key pressed
      key_resp_3.rt = key_resp_3.clock.getTime();
      // a response ends the routine
      continueRoutine = false;
    }
  }
  // check for quit (typically the Esc key)
  if (psychoJS.experiment.experimentEnded || psychoJS.eventManager.getKeys({keyList:['escape']}).length > 0) {
    return psychoJS.quit('The [Escape] key was pressed. Goodbye!', false);
  }
  
  // check if the Routine should terminate
  if (!continueRoutine) {  // a component has requested a forced-end of Routine
    return Scheduler.Event.NEXT;
  }
  
  continueRoutine = false;// reverts to True if at least one component still running
  for (const thisComponent of Instructions_2Components)
    if ('status' in thisComponent && thisComponent.status !== PsychoJS.Status.FINISHED) {
      continueRoutine = true;
      break;
    }
  
  // check for quit (the Esc key)
  if (psychoJS.experiment.experimentEnded || psychoJS.eventManager.getKeys({keyList:['escape']}).length > 0) {
    return quitPsychoJS('The [Escape] key was pressed. Goodbye!', false);
  }
  
  // refresh the screen if continuing
  if (continueRoutine) {
    return Scheduler.Event.FLIP_REPEAT;
  }
  else {
    return Scheduler.Event.NEXT;
  }
}


function Instructions_2RoutineEnd() {
  //------Ending Routine 'Instructions_2'-------
  for (const thisComponent of Instructions_2Components) {
    if (typeof thisComponent.setAutoDraw === 'function') {
      thisComponent.setAutoDraw(false);
    }
  }
  
  // check responses
  if (['', [], undefined].indexOf(key_resp_3.keys) >= 0) {    // No response was made
      key_resp_3.keys = undefined;
  }
  
  psychoJS.experiment.addData('key_resp_3.keys', key_resp_3.keys);
  if (typeof key_resp_3.keys !== 'undefined') {  // we had a response
      psychoJS.experiment.addData('key_resp_3.rt', key_resp_3.rt);
      routineTimer.reset();
      }
  
  // the Routine "Instructions_2" was not non-slip safe, so reset the non-slip timer
  routineTimer.reset();
  
  return Scheduler.Event.NEXT;
}

var EndComponents;
function EndRoutineBegin() {
  //------Prepare to start Routine 'End'-------
  t = 0;
  EndClock.reset(); // clock
  frameN = -1;
  routineTimer.add(3.000000);
  // update component parameters for each repeat
  // keep track of which components have finished
  EndComponents = [];
  EndComponents.push(text_3);
  
  for (const thisComponent of EndComponents)
    if ('status' in thisComponent)
      thisComponent.status = PsychoJS.Status.NOT_STARTED;
  
  return Scheduler.Event.NEXT;
}


function EndRoutineEachFrame() {
  //------Loop for each frame of Routine 'End'-------
  let continueRoutine = true; // until we're told otherwise
  // get current time
  t = EndClock.getTime();
  frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
  // update/draw components on each frame
  
  // *text_3* updates
  if (t >= 0.0 && text_3.status === PsychoJS.Status.NOT_STARTED) {
    // keep track of start time/frame for later
    text_3.tStart = t;  // (not accounting for frame time here)
    text_3.frameNStart = frameN;  // exact frame index
    text_3.setAutoDraw(true);
  }

  frameRemains = 0.0 + 3 - psychoJS.window.monitorFramePeriod * 0.75;  // most of one frame period left
  if (text_3.status === PsychoJS.Status.STARTED && t >= frameRemains) {
    text_3.setAutoDraw(false);
  }
  // check for quit (typically the Esc key)
  if (psychoJS.experiment.experimentEnded || psychoJS.eventManager.getKeys({keyList:['escape']}).length > 0) {
    return psychoJS.quit('The [Escape] key was pressed. Goodbye!', false);
  }
  
  // check if the Routine should terminate
  if (!continueRoutine) {  // a component has requested a forced-end of Routine
    return Scheduler.Event.NEXT;
  }
  
  continueRoutine = false;// reverts to True if at least one component still running
  for (const thisComponent of EndComponents)
    if ('status' in thisComponent && thisComponent.status !== PsychoJS.Status.FINISHED) {
      continueRoutine = true;
      break;
    }
  
  // check for quit (the Esc key)
  if (psychoJS.experiment.experimentEnded || psychoJS.eventManager.getKeys({keyList:['escape']}).length > 0) {
    return quitPsychoJS('The [Escape] key was pressed. Goodbye!', false);
  }
  
  // refresh the screen if continuing
  if (continueRoutine && routineTimer.getTime() > 0) {
    return Scheduler.Event.FLIP_REPEAT;
  }
  else {
    return Scheduler.Event.NEXT;
  }
}


function EndRoutineEnd() {
  //------Ending Routine 'End'-------
  for (const thisComponent of EndComponents) {
    if (typeof thisComponent.setAutoDraw === 'function') {
      thisComponent.setAutoDraw(false);
    }
  }
  return Scheduler.Event.NEXT;
}


function endLoopIteration(thisTrial) {
  // ------Prepare for next entry------
  return function () {
    if (typeof thisTrial === 'undefined' || !('isTrials' in thisTrial) || thisTrial.isTrials) {
      psychoJS.experiment.nextEntry();
    }
  return Scheduler.Event.NEXT;
  };
}


function importConditions(loop) {
  const trialIndex = loop.getTrialIndex();
  return function () {
    loop.setTrialIndex(trialIndex);
    psychoJS.importAttributes(loop.getCurrentTrial());
    return Scheduler.Event.NEXT;
    };
}


function quitPsychoJS(message, isCompleted) {
  psychoJS.window.close();
  psychoJS.quit({message, isCompleted});

  return Scheduler.Event.QUIT;
}
