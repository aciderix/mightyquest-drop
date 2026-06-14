// Generated from the reversed schema catalog (re/tools/gen_types.py).
// direction: request = client->server, response = server->client.

/** both */
export interface AbilityFamily {
  Id: number;
  Name: unknown;
  Ui: unknown;
}

/** unknown */
export interface AbilityFamilySettings {
  Families: unknown;
}

/** unknown */
export interface AbilityLaunchedAssignmentTriggerSpec {
  AbilityId: unknown;
}

/** both */
export interface AbilityLevelAutoAim {
  GameEntityTypePriorities: unknown;
  ParamsList: unknown;
}

/** both */
export interface AbilityLevelAutoAimParam {
  AutoAimType: number;
  EffectRadius: number;
  MaxDistance: number;
  TargetType: number;
}

/** both */
export interface AbilityLevelInfo {
  AbilitySpecContainerId: number;
  Level: number;
}

/** unknown */
export interface AbilityLevelSpec {
  AbilityCastType: unknown;
  AbilityTag: unknown;
  ActiveTime: unknown;
  AttackSpeedFactor: unknown;
  AutoAim: unknown;
  CanBeUsedInstantlyDuringStun: unknown;
  CastCost: unknown;
  Cooldown: unknown;
  DirectedMaxDistance: unknown;
  EffectRadius: unknown;
  HoldAndCast: unknown;
  HoldToPrepare: unknown;
  IgnorePickedTarget: unknown;
  Interruptable: unknown;
  IsConsumable: unknown;
  IsEnabled: unknown;
  IsPassive: unknown;
  MainDamageOperationStatValueSpecTag: unknown;
  ManaCostPerSecond: unknown;
  MaxDistance: unknown;
  MaximumPrepareRotationDuration: unknown;
  NeedFacingTarget: unknown;
  OasisLongDescription: unknown;
  OasisName: unknown;
  OasisShortDescription: unknown;
  OnAbilityEndedOperations: unknown;
  OnAbilityPrepareStartedOperations: unknown;
  OverrideActiveTime: unknown;
  PickingStyle: unknown;
  PositionRestrictionType: unknown;
  PrepareTime: unknown;
  RecoverInterruptWindow: unknown;
  RecoverTime: unknown;
  StartCooldownIfInterrupted: unknown;
  TargetLifeComponentRequired: unknown;
  TargetSearchSpec: unknown;
  TargettingAllianceFilter: unknown;
  TurningRateMultiplier: unknown;
  UpgradeRequirement: unknown;
  UseEntitiesRadius: unknown;
  UseGamepadCursor: unknown;
  Operations: unknown;
}

/** both */
export interface AbilityLevelUiSpec {
  DescriptionFormulas: unknown;
  ManaBuilder: number;
  OasisDescription: number;
  OasisManaBuilderDescription: number;
}

/** both */
export interface AbilityLevelUpgradeRequirement {
  HeroMinimumLevel: number;
  RequiredAbilities: unknown;
}

/** unknown */
export interface AbilityManagerSpec {
  Abilities: unknown;
  BasicAttackSlotIndex: unknown;
  StartWithoutMana: unknown;
}

/** unknown */
export interface AbilityPurchasedAssignmentTriggerSpec {
  AbilityId: unknown;
}

/** unknown */
export interface AbilityRangeValueSpec {
  AbilityIndex: unknown;
}

/** unknown */
export interface AbilitySpec {
  FamilyId: unknown;
  Levels: unknown;
}

/** unknown */
export interface AbilitySpecContainer {
  Type: unknown;
}

/** unknown */
export interface AbilitySpecContainerRef {
  SpecContainerReferenceId: unknown;
}

/** unknown */
export interface AbilityStateSoundEventWrapper {
  StopAtEndOfState: unknown;
}

/** unknown */
export interface AbilityUiSpec {
  Levels: unknown;
  RemoveSpecialWeaponEffectOasisId: unknown;
  SpecialWeaponEffectOasisId: unknown;
  TooltipWeaponDamageMultiplier: unknown;
}

/** unknown */
export interface AbstractAreaOperationSpec {
  AllianceFilter: unknown;
  IsTargetExcluded: unknown;
  MaxTargetsCount: unknown;
  Operations: unknown;
  Position: unknown;
  SearchMethod: unknown;
  Selections: unknown;
  TouchedEntitiesType: unknown;
}

/** unknown */
export interface AbstractFieldBehaviorSpec {
  Booleans: unknown;
}

/** request */
export interface AbstractFriendNewsData {
  RequiredLevel: number;
  RequiredReferralFriends: number;
  Reward: Reward;
}

/** unknown */
export interface AbstractModifierSpec {
  Priority: unknown;
}

/** unknown */
export interface AbstractOperationSpec {
  IsDisabled: unknown;
  OperationLabel: unknown;
  Operations: unknown;
  ResultCombinationType: unknown;
  StopCondition: unknown;
}

/** both */
export interface AbstractShortcutCode {
  CanStillBeTriggeredWithShiftPressedA: boolean;
  IgnoredModifiers: number;
  IsGrabbable: boolean;
  RequiredModifiers: number;
}

/** unknown */
export interface AbstractTargetDefinitionSpec {
  Id: unknown;
  PresetTargetDefinitionId: unknown;
}

/** both */
export interface AcceleratorFactorInfo {
  AcceleratorFactor: number;
}

/** unknown */
export interface AccountArchiveSettings {
  AccountInactivityForArchive: unknown;
  InactiveAccountBatchSize: unknown;
}

/** both */
export interface AccountAttackRegion {
  AttackRegionId: number;
  Status: number;
}

/** both */
export interface AccountBuyBack {
  BuyBackItems: unknown;
}

/** both */
export interface AccountBuyBackSlot {
  Item: unknown;
}

/** both */
export interface AccountExportMetadata {
  ArchiveName: string;
  Description: string;
  NumberOfAccountsByLevel: number;
  SpecificAccountDisplayNames: unknown;
  SpecificAccountIds: number;
  TotalNumberOfAccounts: number;
}

/** both */
export interface AccountForValidation {
  AccountId: number;
  Heroes: unknown;
  Inbox: unknown;
  Inventory: unknown;
  Wallet: Wallet;
}

/** both */
export interface AccountForgedItem {
  ExpirableId: string;
  ForgeMode: number;
  Item: unknown;
  ItemLevelAverage: number;
}

/** both */
export interface AccountHeroStats {
  TimePlayed: number;
  TotalCastlesLooted: number;
  TotalCreaturesKilled: number;
}

/** unknown */
export interface AccountIdAssignmentConditionSpec {
  AccountId: unknown;
}

/** request */
export interface AccountInformation {
  ClientSettings: ClientSettings;
  CommunityEventTimeShift: number;
  CompletedAchievements: number;
  CountryCode: string;
  DefendLog: DefendLog;
  Expirables: Expirable;
  Guild: Guild;
  GuildInvitations: GuildInvitation;
  IsCastleAttackable: boolean;
  LastViewedFreeTrialInfoDate: string;
  News: News;
  ShopSkuModifiers: ShopSkuModifier;
  TargetedAttackAvailableCount: number;
}

/** both */
export interface AccountInformationBase {
  ClientSettings: ClientSettings;
  CommunityEventTimeShift: number;
  CompletedAchievements: number;
  CountryCode: string;
  DefendLog: DefendLog;
  Expirables: Expirable;
  Guild: Guild;
  GuildInvitations: GuildInvitation;
  IsCastleAttackable: boolean;
  LastViewedFreeTrialInfoDate: string;
  News: News;
  ShopSkuModifiers: ShopSkuModifier;
  TargetedAttackAvailableCount: number;
}

/** both */
export interface AccountInventory {
  CastleRenovationItems: unknown;
  ForgedItem: unknown;
  HeroItems: HeroItem;
  InventoryTabCount: number;
  PendingSharedItems: unknown;
}

/** both */
export interface AccountInventorySlot {
  Item: unknown;
  SlotIndex: number;
  StackCount: number;
}

/** both */
export interface AccountLite {
  AccountId: number;
  ActivationStatus: number;
  DisplayName: string;
  Email: string;
  Password: string;
  Privileges: number;
}

/** both */
export interface AccountNameCreatedEventArgs {
  ErrorMessage: string;
  IsSuccess: boolean;
}

/** both */
export interface AccountObjective {
  HasViewed: boolean;
  LastStatusDate: string;
  ObjectiveId: number;
  ProgressionCount: number;
  Status: number;
}

/** both */
export interface AccountObjectivesModel {
  CompletedObjectives: unknown;
  UnlockedObjectives: unknown;
}

/** both */
export interface AccountPremiumCash {
  AccountId: number;
  PremiumCash: number;
}

/** request */
export interface AccountPublicProfile {
  AccountStats: AccountStats;
  AccountSummary: AccountSummary;
  Achievements: Achievement;
  CastleLevel: number;
  CastleStats: CastleStats;
  GamerScore: number;
  Heroes: unknown;
  HeroLevel: number;
  IsCastleAttackable: boolean;
  IsShielded: boolean;
  LeagueId: number;
  SelectedHeroId: number;
  TrophyScore: number;
}

/** both */
export interface AccountQuickStats {
  Privileges: number;
  TrophyScore: number;
  Wallet: Wallet;
}

/** both */
export interface AccountResetInformation {
  DisplayName: string;
  Email: string;
  Id: number;
  ProfileId: string;
}

/** both */
export interface AccountSettings {
  MessagingSettings: MessagingSettings;
}

/** both */
export interface AccountStats {
  AttackTotalIGCWon: number;
  CastlesDefeated: unknown;
  ChallengeCreated: number;
  ChallengeParticipated: number;
  ChallengeWon: number;
  CurrencyAccumulation: unknown;
  DefeatCastleStrike: number;
  DefeatFriendsCastleStrike: number;
  KilledCreatures: unknown;
  TotalCastlesLooted: number;
  TotalCreaturesKilled: number;
  TotalItemsLooted: number;
  TotalPotionsConsumed: number;
}

/** both */
export interface AccountSummary {
  AvatarId: number;
  CastleLevel: number;
  CountryCode: string;
  DisplayName: string;
  GuildHeader: GuildHeader;
  Id: number;
  IsArchived: boolean;
  IsCastleAttackable: boolean;
  LeagueId: number;
  OasisNameId: number;
  SpecialPacks: number;
  SubLeagueId: number;
  TrophyScore: number;
}

/** both */
export interface AccountSummaryForFriendModel {
  AvatarUrl: string;
  Friend: unknown;
  IsCastleAttackable: boolean;
}

/** both */
export interface AccountSummaryForSearchModel {
  AccountSummaryForSearch: unknown;
  AvatarUrl: string;
}

/** both */
export interface AccountSummaryForTools {
  CastleLevel: number;
  CastleThemeId: number;
  CountryCode: string;
  DisplayName: string;
  Email: string;
  Id: number;
  IsCastleAttackable: boolean;
  LastShownWelcomePageDate: string;
  LeagueId: number;
  PlatformId: string;
  Privileges: number;
  ProfanityFiltering: boolean;
  ProfileId: string;
  SelectedHeroId: number;
  SpecialPacks: number;
  SubLeagueId: number;
  TargetedAttackAvailableCount: number;
  TrophyScore: number;
}

/** both */
export interface AccountUiCacheViewModel {
  AccountId: number;
  AvatarUrl: string;
  CurrentHeroId: number;
  DisplayName: string;
  SpecialPackModel: SpecialPackModel;
}

/** both */
export interface Achievement {
  Count: number;
}

/** both */
export interface AchievementCompletedModel {
  Achievement: Achievement;
}

/** request */
export interface AchievementCompletedNotification {
  AchievementId: number;
  GamerScoreToAdd: number;
  HasUiNotification: boolean;
  Index: number;
  NotificationType: number;
}

/** both */
export interface AchievementContainer {
  Achievements: Achievement;
  CompletedCount: number;
  TotalCount: number;
}

/** request */
export interface AchievementProgression {
  Achievement: Achievement;
  CompletionDate: string;
  CompletionDateFriendly: string;
  CompletionPercentage: number;
}

/** unknown */
export interface AchievementSettings {
  Achievements: unknown;
}

/** unknown */
export interface ActionAggroBehaviorSpec {
  Target: unknown;
}

/** unknown */
export interface ActionBehaviorSpec {
  DelayBeforeStartMax: unknown;
  DelayBeforeStartMin: unknown;
  Interruptible: unknown;
  IsContinuous: unknown;
}

/** both */
export interface ActionButtonModel {
  NavigationUrl: string;
  OasisId: number;
}

/** unknown */
export interface ActionChargeBehaviorSpec {
  Target: unknown;
}

/** unknown */
export interface ActionFaceToBehaviorSpec {
  Pth: unknown;
  Target: unknown;
}

/** unknown */
export interface ActionFearBehaviorSpec {
  Duration: unknown;
  Target: unknown;
}

/** unknown */
export interface ActionLeashBehaviorSpec {
  LeashDistance: unknown;
  UseTotemLeashDistance: unknown;
}

/** unknown */
export interface ActionMoveToBehaviorSpec {
  HysteresisModifier: unknown;
  MovementSpeedMultiplier: unknown;
  SpeedScaleMaxDistance: unknown;
  SpeedScaleMinDistance: unknown;
  StopDistance: unknown;
  SucceedOnArrival: unknown;
  Target: unknown;
  UseEntitiesRadius: unknown;
}

/** unknown */
export interface ActionRegenerationBehaviorSpec {
  ConditionTargetIsUnreachable: unknown;
  FearDistance: unknown;
  FearDuration: unknown;
  MaxLifeRatio: unknown;
  MinLifeRatio: unknown;
  Target: unknown;
}

/** unknown */
export interface ActionUseAbilityBehaviorSpec {
  AbilityIndex: unknown;
  ActionLineClearCheckWidth: unknown;
  AdjustFacingIfNeeded: unknown;
  MoveIntoAbilityRangeIfNeeded: unknown;
  NeedActionLineClear: unknown;
  Target: unknown;
}

/** request */
export interface ActivateConsumableCommand {
  ConsumableTemplateId: number;
  CurrentStackCount: number;
  ForceActivation: boolean;
  InventorySlotIndex: number;
}

/** request */
export interface ActivateConsumableOnItemCommand {
  HeroItemSlot: number;
  InventorySlotIndex: number;
}

/** unknown */
export interface ActivateDeactivatePickingAssignmentActionSpec {
  Activate: unknown;
  TargetEntitySearch: unknown;
}

/** unknown */
export interface ActivateDeactivatePickingOperationSpec {
  Activate: unknown;
}

/** both */
export interface ActiveConsumable {
  ConsumableType: number;
  ExpirableId: string;
  InitialDuration: number;
  TemplateId: number;
}

/** both */
export interface ActiveConsumableModel {
  ConsumableType: number;
  DisplayRemainingTime: boolean;
  IconUrl: string;
  InitialDuration: number;
  RemainingTime: number;
  TemplateId: number;
}

/** both */
export interface ActivityBucket {
  AttackableCastleStatus: number;
  BucketId: number;
  MinSize: number;
  UserActivity: number;
}

/** request */
export interface AddCastleCreatureCommand {
  AggroPropagationOffsetX: number;
  AggroPropagationOffsetZ: number;
  TotemCastleBuildableId: number;
}

/** request */
export interface AddCastleInventoryItemCommand {
  ConsumedHeroInventory: unknown;
  SkuCode: string;
}

/** request */
export interface AddCastleTrapCommand {
  BeatIndex: number;
  PowerSupplyCastleBuildableId: number;
}

/** request */
export interface AddCastleTriggerCommand {
  SizeX: number;
  SizeY: number;
}

/** unknown */
export interface AddItemsToInventoryAssignmentActionSpec {
  InventoryItems: unknown;
}

/** unknown */
export interface AddLifeShieldOperationSpec {
  Duration: unknown;
  Value: unknown;
}

/** unknown */
export interface AddOrientationSpec {
  Value1: unknown;
  Value2: unknown;
}

/** unknown */
export interface AddValueSpec {
  Value1: unknown;
  Value2: unknown;
}

/** unknown */
export interface AddVectorSpec {
  Value1: unknown;
  Value2: unknown;
}

/** both */
export interface AdminBuildingUpgrade {
  BuildingId: number;
  FinalRank: number;
  SpecContainerId: number;
  StartRank: number;
}

/** both */
export interface AdminCastleStats {
  AttackCount: number;
  SuccessfulAttackCount: number;
  WinRatio: number;
}

/** unknown */
export interface AggroSpec {
  AggroConeAngleOverride: unknown;
  AggroConeRadiusOverride: unknown;
  AggroPropagationOffsetOverride: unknown;
  AggroPropagationRangeOverride: unknown;
  AggroRangeOverride: unknown;
}

/** unknown */
export interface AiControllerSpec {
  Behavior: unknown;
  CheckPlayerDistanceToDoTasks: unknown;
  EnableInBuild: unknown;
  PrioritizeRecurringTasks: unknown;
}

/** unknown */
export interface AimedCannonSpec {
  SearchAngleTolerance: unknown;
  SearchDistance: unknown;
}

/** both */
export interface AlertedCountChangedEventArgs {
  CurrentAlertedCount: number;
  PreviousAlertedCount: number;
}

/** both */
export interface AllLifeShieldsUpdatedEventArgs {
  HasLastLifeShieldDurationAlmostEnded: boolean;
  LifeShieldUpdates: LifeShieldUpdate;
}

/** both */
export interface AlternateLocaleFont {
  Locales: unknown;
  SynergyFontTexture: string;
}

/** unknown */
export interface AndBooleanSpec {
  Booleans: unknown;
}

/** both */
export interface AntiCheatAttackInfo {
  AttackId: string;
  AttackInfo: AttackInfo;
}

/** both */
export interface AntiCheatEndAttackParams {
  AttackId: string;
  DeterminismBreak: boolean;
  Duration: number;
  EndAttackParams: EndAttackParams;
}

/** both */
export interface ArchetypeStatModel {
  CompareValue: number;
  FormatValueAsPercentage: boolean;
  FormatValuePrecision: number;
  MaxValue: number;
  Name: string;
  ShowAsSlider: boolean;
  ShowTextValue: boolean;
  Value: number;
}

/** request */
export interface ArchitectOfficeBuildingInfoDataModel {
  CurrentMaxRooms: number;
  MaxMaxRooms: number;
}

/** request */
export interface ArchitectOfficeBuildingUpgradePopupDataModel {
  NewMaxRooms: number;
}

/** request */
export interface ArmorArchetype {
  Damage: number;
  Health: number;
  Resistance: number;
  Id: number;
  Name: unknown;
  Probability: number;
}

/** unknown */
export interface AssetViewerSettings {
  Back: unknown;
  Body: unknown;
  FilterAssetsForHero: unknown;
  Hand: unknown;
  Head: unknown;
  Shoulder: unknown;
  Weapon: unknown;
  WeaponFx: unknown;
}

/** unknown */
export interface AssignmentActionSpec {
  Conditions: unknown;
  Disabled: unknown;
  Duration: unknown;
  EndTriggers: unknown;
  EndType: unknown;
  StartDelay: unknown;
  StartType: unknown;
  DisableCastleValidation: unknown;
}

/** unknown */
export interface AssignmentCompletedAssignmentTriggerSpec {
  AssignmentId: unknown;
}

/** request */
export interface AssignmentCompletedNotification {
  AssignmentId: number;
}

/** unknown */
export interface AssignmentConditionSpec {
  IsNot: unknown;
  SpecContainerIds: unknown;
  SpecContainerType: unknown;
}

/** both */
export interface AssignmentGroup {
  Id: number;
  Name: string;
}

/** unknown */
export interface AssignmentSettings {
  Groups: unknown;
  HeroSelectionAssignmentId: unknown;
  NueCompletionAssignmentIds: unknown;
}

/** unknown */
export interface AssignmentSpec {
  Actions: unknown;
  Enable: unknown;
  ExitTrigger: unknown;
  ForceCompletionOnExit: unknown;
  GrantedAccess: unknown;
  GroupId: unknown;
  IsDiscardedOnCompletion: unknown;
  Trigger: unknown;
}

/** unknown */
export interface AssignmentSpecContainer {
  Type: unknown;
}

/** unknown */
export interface AssignmentTriggerSpec {
  Conditions: unknown;
  IsServerTrigger: unknown;
  BuildingSpecContainerIds: unknown;
  MaxRank: unknown;
  MinRank: unknown;
}

/** unknown */
export interface AssignmentsCompletedAssignmentConditionSpec {
  Assignments: unknown;
}

/** response */
export interface AttackAdvisorSettings {
  ActiveCastlesCount: number;
  ActivityBuckets: number;
  ActivityBucketsAdvisorLifetime: string;
  AttackRegions: number;
  BrandedCastleDisplayedPerRegion: number;
  CastleCountAfterLessAttackedSelection: number;
  CastleCountAfterRetrieval: number;
  CastleCountAfterTrophyGainFiltering: number;
  LastConnectionMaxThreshold: string;
  LastConnectionMinThreshold: string;
  LessAttackedCastlesCount: number;
  MaxSuggestionCountByLevel: number;
  MaxValidableCastleCountByLevel: number;
  MinAttackablePvpCastleLevel: number;
  MinAttackCountForBestHeroDisplay: number;
  SampleGroupMachineLearning: number;
  TrophyGainBuckets: number;
  ValidableCastleTimeToLive: string;
}

/** unknown */
export interface AttackAssignmentConditionSpec {
  CastleId: unknown;
  CastleModeMask: unknown;
}

/** unknown */
export interface AttackAssignmentTriggerSpec {
  CastleId: unknown;
  CastleModeMask: unknown;
  ExcludeTestAttack: unknown;
  CompletionTypeMask: unknown;
}

/** unknown */
export interface AttackExitedAssignmentTriggerSpec {
  CompletionTypeMask: unknown;
}

/** unknown */
export interface AttackGameStateConfig {
  AttackRegionId: unknown;
  AttackSource: unknown;
  AttackType: unknown;
  CustomThemeId: unknown;
  GameStateModifier: unknown;
  RevengeAttackId: unknown;
  UbisoftCompetitionId: unknown;
  WorldName: unknown;
}

/** both */
export interface AttackImpactSoundInfos {
  HeroImpactSound: unknown;
  OtherImpactSound: unknown;
}

/** both */
export interface AttackImpactSoundLevelsProfile {
  LevelsMaxDamageRatios: number;
}

/** both */
export interface AttackImpactSoundSettings {
  AttackImpactSoundLevelsPerArmorType: number;
  AttackImpactSoundLevelsProfiles: AttackImpactSoundLevelsProfile;
  AttackImpactSoundsById: unknown;
  CriticalHitImpactSound: unknown;
  ReflectedDamageImpactSound: unknown;
}

/** both */
export interface AttackInfo {
  AdjustedHeroLevel: number;
  AttackerActiveConsumables: unknown;
  AttackerDisplayName: string;
  AttackId: string;
  AttackRandomSeed: number;
  AttackType: number;
  AttackUserSettings: AttackUserSettings;
  Castle: Castle;
  CastleHeartRank: number;
  CastleType: number;
  CastleValidationDuration: number;
  CreatureLoot: unknown;
  DecorationLoot: unknown;
  DefenderActiveConsumables: unknown;
  DefenderSpecialPacks: number;
  FirstResurrectionCost: number;
  FreeInventorySlotsCount: number;
  Hero: Hero;
  InventoryConsumablesInfo: InventoryConsumablesInfo;
  IsResurrectionAllowed: boolean;
  IsRevenge: boolean;
  IsShielded: boolean;
  IsTargetedAttack: boolean;
  IsTutorial: boolean;
  Level: number;
  LoseTrophyCooldownTimer: string;
  StealableMines: StealableMine;
  TargetedAttackAvailableCount: number;
  TrapLoot: unknown;
  TreasureRoomGoldRatio: number;
  TreasureRoomHeroItem: unknown;
  TreasureRoomLifeForceRatio: number;
  TreasureRoomReward: unknown;
  TreasureRoomStealableIGC: unknown;
  TreasureRoomStealableLifeForce: unknown;
  TrophyScoreDefender: number;
  TrophyScoreGain: number;
  TrophyScoreLost: number;
  TrophyScoreLostWithoutCooldown: number;
  TrophyScoreRestartAttackGain: number;
  TrophyScoreRestartAttackLost: number;
  TrophyScoreRestartLostWithoutCooldown: number;
  UbisoftCompetitionBestTime: number;
  UbisoftCompetitionId: number;
  UnlockedEmotes: number;
  UnlockedSpells: unknown;
  VictoryConditionRewardRatios: number;
}

/** request */
export interface AttackInfoModel {
  AttackerSpecialPackModel: unknown;
  AttackInfo: AttackInfo;
  DefenderSpecialPackModel: unknown;
  IsTestAttack: boolean;
}

/** both */
export interface AttackLoadedEventArgs {
  HudHeroInfoModel: HudHeroInfoModel;
}

/** unknown */
export interface AttackOperationSpec {
  BakedDamageInfo: unknown;
}

/** both */
export interface AttackRegion {
  AttackRegionId: number;
  BossCastleId: number;
  BossName: number;
  DebugName: string;
  HasMLPrediction: boolean;
  IsCompetitionRegion: boolean;
  IsFriendRegion: boolean;
  LevelMax: number;
  LevelMin: number;
  Name: number;
  OverPosX: number;
  OverPosY: number;
  ShowUbisoftCastle: boolean;
  ShowUserCastle: boolean;
  ShowValidableCastle: boolean;
}

/** request */
export interface AttackRegionCompletedNotification {
  CompletedAttackRegionId: number;
  UnlockedAttackRegionId: number;
}

/** both */
export interface AttackRegionModel {
  AttackRegionId: number;
  BossCastleId: number;
  BossName: string;
  CanAfford: boolean;
  IsCompetitionRegion: boolean;
  IsFriendRegion: boolean;
  LevelMax: number;
  LevelMin: number;
  OverPosX: number;
  OverPosY: number;
  RegionName: string;
  ShowMoreCastleSkus: unknown;
  Status: number;
}

/** request */
export interface AttackRegionUnlockedObjectiveRequirement {
  AttackRegionId: number;
}

/** both */
export interface AttackRegionsChangedEventArgs {
  UpdatedAttackRegions: unknown;
}

/** both */
export interface AttackRegionsViewModel {
  AttackRegions: AttackRegion;
}

/** both */
export interface AttackReplay {
  AccountID: number;
  AttackHistoryIndex: number;
}

/** unknown */
export interface AttackReplayFromServerGameStateConfig {
  AttackId: unknown;
  Repeat: unknown;
}

/** unknown */
export interface AttackReplayGameStateConfig {
  Repeat: unknown;
  ReplayFileName: unknown;
}

/** request */
export interface AttackReportPanelNavigationModel {
  RewardModel: RewardModel;
}

/** both */
export interface AttackReportPredefinedComment {
  CommentTextOasisIDs: number;
  LayerName: string;
  ShortDescriptionOasisID: number;
}

/** both */
export interface AttackSelectionByLevelResult {
  Castles: Castle;
  Level: number;
}

/** request */
export interface AttackSelectionCastlePanelNavigationModel {
  AttackRegionModel: AttackRegionModel;
  CastleInfoSummary: CastleInfoSummary;
  CastleObjectiveStatusModel: CastleObjectiveStatusModel;
  PanelName: number;
  SpecialPackModel: SpecialPackModel;
}

/** both */
export interface AttackSelectionCastleRefreshedEventArgs {
  CastleInfo: CastleInfo;
  DefenderSpecialPackModel: unknown;
}

/** request */
export interface AttackSelectionPlayerMiniCastlePanelNavigationModel {
  AreRequiredMaterialsInHeroInventory: boolean;
  IsOpalPanel: boolean;
  PanelName: number;
}

/** both */
export interface AttackSelectionResult {
  BossCastle: unknown;
  CastlesByLevel: unknown;
}

/** request */
export interface AttackSelectionResultModel {
  AttackRegion: AttackRegion;
  Result: unknown;
  SpecialPackModels: SpecialPackModel;
}

/** response */
export interface AttackSettings {
  ActionLineCheckHeight: number;
  AggroConeAngle: number;
  AggroConeRadius: number;
  AggroPropagationOffset: number;
  AggroPropagationRange: number;
  AggroRange: number;
  AttackerDeathPopupDelay: number;
  AttackSpeedTable: number;
  AttackTimerStartAnimationTimeExpired: number;
  BasicAttackBuffId: number;
  BigFlinchMinDamageRatio: number;
  ChallengeCountdownDuration: number;
  CorpseDuration: number;
  CraftingMaterialMineEmptyItemDropCount: number;
  CraftingMaterialMineEmptyItemDropQuality: unknown;
  CraftingMaterialMineItemDropCount: number;
  CreatureBasicAttackBuffId: number;
  CreatureCatchUpBuffId: number;
  CreatureRoomBuildablesCreationInterval: number;
  CriticalHitCameraShakeAnimation: number;
  DefaultAttackRange: number;
  DefaultCreatureCreationPriorityCoefficient: number;
  DefaultFacingDamping: number;
  DefaultRoomBuildableEntitiesCreationDistance: number;
  DefaultSpawnedEntityAggroTarget: number;
  DoorTriggerCollisionDistance: number;
  EscapeDelayToMarkAsDefeat: number;
  FarmGruntThreshold: number;
  FarmMpsThreshold: number;
  FarmTrapIds: number;
  FightDynamics: number;
  GainTrophyCooldownTimerDuration: string;
  HealthOrbBuffId: number;
  HeroManaDescriptionOasisIds: unknown;
  HeroRegenerationDuration: number;
  HeroTrapXpRewardShape: number;
  InputBufferingDuration: number;
  InvalidActionsFeedbacks: number;
  LeashBehaviorBuffSpecContainerIds: number;
  LifeShieldDurationRatioEndAnimation: number;
  LootAnimationDuration: number;
  LootAttractionDelay: number;
  LootAttractionDistance: number;
  LootBlinkDuration: number;
  LootDelayBetweenEachDrop: number;
  LootDropDelay: number;
  LootDropMaxDistance: number;
  LootDropMinDistance: number;
  LootDropSectorCircleArc: number;
  LootDropSectorCircleArcStartAngle: number;
  LootEffectSpecContainerIds: unknown;
  LootForcedAttractionDelay: number;
  LootForcedAttractionVelocity: number;
  LootRadius: number;
  LoseTrophyCooldownTimerDuration: string;
  LossPonderationTable: number;
  MaxAggroPropagationDistanceOfPathFindResult: number;
  MaxCpCreatureCreation: number;
  MaximumAllowedAttackTimeDiscrepancy: string;
  MaximumSpawnDelay: number;
  MaxLevelDifferenceForBossAttack: number;
  MaxMpsStored: number;
  MinCastleLevelForPVPAttack: number;
  MineDestroyedTimeBonus: string;
  MineEmptyAmountDrop: number;
  MineLossPonderationTable: number;
  MinePeriodStealableAmountInSeconds: number;
  MineShieldedAmoutDrop: number;
  MinimumCooldownAfterReduction: number;
  MinimumKnockbackDuration: number;
  MinimumManaCostAfterReduction: number;
  MinimumMoveDistance: number;
  MinimumMoveDistanceHysteresisModifier: number;
  MinimumSpawnDelay: number;
  MoveAndCastDetectionAngle: number;
  MovementSpeedTable: number;
  MultiKillTimeInterval: number;
  NavigationCollisionRaycastLength: number;
  NavigationCollisionTurnDuration: number;
  NavigationCollisionTurnSpeed: number;
  NavigationMinimumStopDistance: number;
  NextAttackedUnitSearchRadius: number;
  PetLootActive: boolean;
  PlayerDistanceToDoTasks: number;
  PositionRestrictionDistanceFlexibilities: unknown;
  PotionUsageRestrictions: number;
  PremiumCashMineLossAmount: number;
  PremiumCashMineLossPonderationTable: number;
  PresetTargetDefinitions: unknown;
  QueueCoolingDownAbilities: boolean;
  RandomizedLifeValueRandomCallsCount: number;
  RandomizedLifeValueRangeModifier: number;
  RegenerationBehaviorBuffSpecContainerId: number;
  ResistanceSettings: number;
  ResurrectBuffId: number;
  RoomBuildableEntitiesCreationDistanceByType: unknown;
  SelectNextAttackedUnitDelay: number;
  SingleClickToleranceTime: number;
  SleepingCreatureCreationPriorityCoefficient: number;
  SmallFlinchMinDamageRatio: number;
  SteamScreenshotAggroedMobSize: number;
  SteamScreenshotsCreatureRanks: unknown;
  SteamScreenshotsEnabled: boolean;
  StorageChestCageRadius: number;
  SubstituteActionMoveToSpeedMultiplier: number;
  TargetedAttackMaxCount: number;
  TargetedAttackReloadDuration: string;
  TargetEntityHealthBarDelayInSeconds: number;
  TimerEndingCountdownDurationInSeconds: number;
  TreasureDoorEffectSpecContainerId: number;
  TreasureRoomEntranceTriggerFieldName: string;
  TrophyMaxPotionsLimit: number;
  UbisoftCastleMineAmountDrop: number;
  UseEntitiesRadiusForDistanceChecks: boolean;
}

/** both */
export interface AttackSpeed {
  Id: number;
  Name: unknown;
  SpeedFrom: number;
  SpeedTo: number;
}

/** request */
export interface AttackStartCountdownPanelNavigationModel {
  CountdownStep: number;
}

/** both */
export interface AttackUserSettings {
  MinHeroItemQualityToPickUp: number;
  UseCameraDamping: boolean;
}

/** unknown */
export interface AttackableCastleAssignmentConditionSpec {
  IsNot: unknown;
}

/** request */
export interface AttackerAvatarUpdatedNotification {
  AttackerAccountId: number;
  AttackerAvatarId: number;
}

/** response */
export interface AttackerRewardSettings {
  BossLootRatio: number;
  CrownsDiminishingReturns: number;
  DeathResetTimerDuration: string;
  HealthOrbFragmentsModifierTable: number;
  LootTransfereCostsPerLevel: number;
  MineDestroyedVictoryCondition: number;
  RareDefenseIngredientBonusFactor: number;
  RareDefenseIngredientBonusMinimumRatio: number;
  RareDefenseIngredientColorList: number;
  SmartLootWeeklyContentStopLimit: number;
  TreasureRoomGoldDropValueModifier: number;
  TreasureRoomGoldPiles: number;
  TreasureRoomLifeForceDropValueModifier: number;
  TreasureRoomMaxGoldRatio: number;
  TreasureRoomMaxLifeForceRatio: number;
  TreasureRoomMinGoldRatio: number;
  TreasureRoomMinLifeForceRatio: number;
  VictoryConditionRewardRatios: number;
}

/** unknown */
export interface AttractionFieldBehaviorSpec {
  AttractionSpeedExponentCoefficient: unknown;
  MaxAttractionSpeedCoefficient: unknown;
  MinAttractionSpeedCoefficient: unknown;
}

/** unknown */
export interface AudioAbilityAnimTagFxSpec {
  StartSound: unknown;
}

/** unknown */
export interface AudioAbilityEquipmentQualityAnimTagFxSpec {
  ItemQualityLevels: unknown;
  Slot: unknown;
}

/** unknown */
export interface AudioAbilityLevelSpec {
  ActiveSound: unknown;
  ChargeUpInterruptedSound: unknown;
  EndSound: unknown;
  InstantSound: unknown;
  PrepareSound: unknown;
  RecoverSound: unknown;
  StartSound: unknown;
}

/** unknown */
export interface AudioAbilitySpec {
  Levels: unknown;
}

/** unknown */
export interface AudioAttackImpactSpec {
  ImpactSoundId: unknown;
}

/** unknown */
export interface AudioBossFightMusicOverrideSpec {
  BossFightMusic: unknown;
}

/** unknown */
export interface AudioBuffSpec {
  BuffAddedSound: unknown;
  BuffRemovedSound: unknown;
  HeroBuffAddedSoundPreset: unknown;
  HeroBuffRemovedSoundPreset: unknown;
}

/** unknown */
export interface AudioBuffedFootStepSpec {
  BuffedFootStepSound: unknown;
}

/** unknown */
export interface AudioBuildSoundsOverrideSpec {
  BuiltEntityDeleteSound: unknown;
  BuiltEntityDropSound: unknown;
  BuiltEntityPickupSound: unknown;
  BuiltEntityRotateSound: unknown;
  BuiltEntitySelectionSound: unknown;
  BuiltEntitySnapSound: unknown;
}

/** unknown */
export interface AudioDamageSpec {
  ArmorTag: unknown;
  AttackImpactSoundLevelsProfileType: unknown;
  CriticalHitSound: unknown;
  DeathSound: unknown;
  NormalHitSound: unknown;
}

/** unknown */
export interface AudioDestructibleLevelSpec {
  States: unknown;
}

/** unknown */
export interface AudioDestructibleSpec {
  Levels: unknown;
}

/** unknown */
export interface AudioDestructibleStateSpec {
  StateEnterSound: unknown;
  StateExitSound: unknown;
}

/** unknown */
export interface AudioExtraModifierCollectionsSpec {
  CollectionsByAnimName: unknown;
}

/** unknown */
export interface AudioFieldSpec {
  EntityEnterFieldSound: unknown;
  EntityLeaveFieldSound: unknown;
  FieldShowSound: unknown;
  FieldVanishSound: unknown;
  LastEntityLeaveFieldSound: unknown;
}

/** both */
export interface AudioInfoTracking {
  HasAudioDeviceAvailable: boolean;
}

/** unknown */
export interface AudioLabelOperationFxSpec {
  OperationLabel: unknown;
  ReceiverType: unknown;
  Sound: unknown;
}

/** unknown */
export interface AudioMultiStatModifierFxSpec {
  StatModifiersSounds: unknown;
}

/** unknown */
export interface AudioOperationFxSpec {
  LabelOperationSounds: unknown;
}

/** unknown */
export interface AudioPersistentEntityFxSpec {
  CreateSound: unknown;
  DestroySound: unknown;
}

/** unknown */
export interface AudioRoomAmbienceSpec {
  RoomAmbienceSound: unknown;
}

/** unknown */
export interface AudioSettings {
  AttackImpactSoundsSettings: unknown;
  BusInfos: unknown;
  DefaultAmbienceCrossFadeDuration: unknown;
  FootstepsSoundSettings: unknown;
  GameStateSoundPresetsSettings: unknown;
  GeneralAttackSounds: unknown;
  GeneralBuildSounds: unknown;
  GeneralLobbySounds: unknown;
  GenericSounds: unknown;
  HeroCriticalHealthRatio: unknown;
  HeroVoicesSounds: unknown;
  KeepAudioOnFocusLost: unknown;
  MusicCrossFadeDuration: unknown;
  PanelSoundPresetsSettings: unknown;
  RoomAmbienceCrossFadeDuration: unknown;
  UserInterfaceSounds: unknown;
  VoiceOverSounds: unknown;
}

/** unknown */
export interface AudioStatModifierFxSpec {
  StartSound: unknown;
  StatType: unknown;
  StopSound: unknown;
}

/** unknown */
export interface AudioTrapSpec {
  TrapActivatedSound: unknown;
  TrapDeactivatedSound: unknown;
}

/** unknown */
export interface AuraCarrierSpec {
  Aura: unknown;
}

/** unknown */
export interface AuraSpec {
  AllianceFilter: unknown;
  Buff: unknown;
  Radius: unknown;
}

/** unknown */
export interface AuraSpecContainer {
  Type: unknown;
  SpecContainerReferenceId: unknown;
}

/** unknown */
export interface AuraSpecContainerRef {
  SpecContainerReferenceId: unknown;
}

/** both */
export interface Avatar {
  AnimationName: string;
  DebugName: string;
  IconUrl: string;
  Id: number;
  IsPrivate: boolean;
  LayerName: string;
}

/** request */
export interface AvatarEditPanelPanelNavigationModel {
  AvatarCategory: number;
  IsOpalPanel: boolean;
  PanelName: number;
}

/** request */
export interface AvatarRewardItem {
  AvatarId: number;
}

/** unknown */
export interface AvatarSettings {
  Avatars: unknown;
  GuildsIconsAnimations: unknown;
  GuildsIconsLarge: unknown;
  GuildsIconsSmall: unknown;
  GuildsIconsSquare: unknown;
}

/** request */
export interface AvatarUnlockedNotification {
  AvatarId: number;
  Index: number;
  NotificationType: number;
}

/** both */
export interface AvatarUpdatedEventArgs {
  AvatarCategory: number;
  AvatarId: number;
  IconUrl: string;
}

/** request */
export interface AvatarUpdatedNotification {
  AvatarId: number;
  Index: number;
  NotificationType: number;
}

/** both */
export interface AvatarsModel {
  Avatars: Avatar;
  CurrentAvatar: unknown;
}

/** both */
export interface BakedDamageInfo {
  CriticalHitChance: number;
  CriticalHitDamageMultiplier: number;
  SourceEntityId: number;
  SourceLevel: number;
}

/** both */
export interface BakedSpellInfo {
  Alliance: number;
  SourceLevel: number;
}

/** unknown */
export interface BallisticAutoPitchMoveSpec {
  Destination: unknown;
  Gravity: unknown;
  Speed: unknown;
}

/** unknown */
export interface BallisticMoveSpec {
  Gravity: unknown;
  Orientation: unknown;
  Pitch: unknown;
  Speed: unknown;
  ReplacedDebugName: unknown;
}

/** unknown */
export interface BaseHarvestingSpec {
  ShouldDelayHarvest: unknown;
}

/** both */
export interface BaseTextualFeedback {
  DebugMsg: string;
  OasisId: number;
}

/** unknown */
export interface BasicDamageModifierSpec {
  Bonus: unknown;
  DamageSourceTypeFilter: unknown;
  Multiplier: unknown;
}

/** unknown */
export interface BasicFloatModifierSpec {
  Bonus: unknown;
  Multiplier: unknown;
}

/** request */
export interface BattleLogEntry {
  AttackDurationInMilliseconds: number;
  AttackerAccountSummary: unknown;
  AttackerTrophyScoreVariation: number;
  AttackId: string;
  AttackStartDateTime: string;
  AttackType: number;
  CastleLevel: number;
  CastleRating: number;
  CompletionType: number;
  DefenderAccountSummary: unknown;
  DefenderTrophyScoreVariation: number;
  HasReplay: boolean;
  HeroLevel: number;
  HeroSpecContainerId: number;
  IsCastleAttackable: boolean;
  IsRevengeAttack: boolean;
  IsShielded: boolean;
  IsTargetedAttack: boolean;
  Message: Message;
  PillagedMines: PillagedMine;
  PotionUsed: number;
  ResurrectionCount: number;
  RevengeStatus: number;
  StolenIGC: unknown;
  StolenLifeForce: unknown;
  VictoryConditionLevel: number;
  VictoryConditionRewardRatios: number;
  VictoryConditionType: number;
}

/** request */
export interface BattleLogEntryAddedNotification {
  Entry: unknown;
  LastValidEntryDate: string;
}

/** request */
export interface BattleLogEntryDeletedNotification {
  LastValidEntry: string;
}

/** request */
export interface BattleLogEntryModel {
  AttackDurationInMilliseconds: number;
  AttackId: string;
  AttackStartDateTime: string;
  AttackType: number;
  CastleLevel: number;
  CastleRating: number;
  CompletionType: number;
  HeroLevel: number;
  HeroSpecContainerId: number;
  HomeAccountSummary: unknown;
  HomeTrophyScoreVariation: number;
  IsHomeAttack: boolean;
  IsReplayEnabled: boolean;
  IsShielded: boolean;
  Message: string;
  PotionUsedCount: number;
  ResurrectionCount: number;
  RevengeStatus: number;
  StolenIGC: unknown;
  StolenLifeForce: unknown;
  VictoryConditionLevel: number;
  VisitorAccountSummary: unknown;
}

/** request */
export interface BattleLogEntryUpdatedNotification {
  AttackId: string;
  RevengeStatus: number;
}

/** both */
export interface BattleLogNewItemCountChangedEventArgs {
  NewDefendLogEntry: number;
}

/** request */
export interface BattleLogPanelNavigationModel {
  FriendsOnly: boolean;
  ReplayAttackId: string;
  Tab: number;
}

/** unknown */
export interface BeamFieldSpec {
  CollisionMaskAll: unknown;
  CollisionMaskAny: unknown;
  MaxLength: unknown;
  StopperCollisionMask: unknown;
  Width: unknown;
}

/** both */
export interface BehaviorCategory {
  Id: number;
  Name: unknown;
  Ui: unknown;
}

/** unknown */
export interface BehaviorCategorySettings {
  Creatures: unknown;
  Traps: unknown;
}

/** unknown */
export interface BehaviorSpec {
  Conditions: unknown;
  IsDisabled: unknown;
  DelayBeforeStartMax: unknown;
  DelayBeforeStartMin: unknown;
  Interruptible: unknown;
  IsContinuous: unknown;
}

/** unknown */
export interface BehaviorTreeBehaviorSpec {
  TargetDefinitions: unknown;
}

/** unknown */
export interface BlinkTeleportOperationSpec {
  StopperCollisionMaskAll: unknown;
  StopperCollisionMaskAny: unknown;
  TargetPosition: unknown;
}

/** unknown */
export interface BooleanSpec {
  Booleans: unknown;
}

/** request */
export interface BoostCastleInventoryItemCommand {
  ConsumedHeroInventory: unknown;
  ExpirableId: string;
  Id: number;
  ItemType: number;
  SkuCode: string;
}

/** unknown */
export interface BoostCommunityEvent {
  ConsumableTemplateId: unknown;
  AttackIncreasedGold: unknown;
  MineIncreasedGold: unknown;
}

/** request */
export interface BoostConsumableTemplate {
  IncreasedXp: number;
}

/** request */
export interface BoostIconPanelNavigationModel {
  IsOpalPanel: boolean;
  IsTotem: boolean;
  PanelName: number;
}

/** both */
export interface BoostInfoModel {
  ActiveBoostDurationLeft: number;
  ActiveBoostTotalDuration: number;
  BoostDescription: string;
  BoostDuration: number;
  BoostId: number;
  BoostLayerName: string;
  BoostName: string;
  CanAffordCurrency: boolean;
  CanAffordMaterials: boolean;
  Cost: unknown;
  CraftingMaterials: CraftingMaterial;
  CurrentBoostedCreatureCount: number;
  IsBoostable: boolean;
  IsBoostPending: boolean;
  IsTotem: boolean;
  MaxBoostedCreatureCount: number;
  SubjectName: string;
}

/** both */
export interface BootConfig {
  AdditionalLaunchCommandLine: number;
  AttackSource: number;
  CastleLoadConfig: CastleLoadConfig;
  CompressedGPSettings: boolean;
  DistributionServiceUrl: string;
  EnvironmentName: string;
  GameLanguage: string;
  GameStateModifier: number;
  GameStateType: number;
  GameWebsiteUrl: string;
  PlayerLoadConfig: PlayerLoadConfig;
  ReplayModeConfig: ReplayModeConfig;
  ServerLatency: number;
  ServerLatencyRandomized: boolean;
  UILatency: number;
  UseGamePatching: boolean;
  WorldName: string;
}

/** request */
export interface BossKilledFriendNewsData {
  AttackRegionId: number;
  BossLevel: number;
  BossName: string;
}

/** both */
export interface BoundingRect {
  MaxX: number;
  MaxY: number;
  MinX: number;
  MinY: number;
}

/** unknown */
export interface BoxShapeSpec {
  Height: unknown;
  Length: unknown;
  Width: unknown;
}

/** both */
export interface Branch {
  GamePublicationLabelMajorSuffix: number;
  GamePublicationLabelPrefix: string;
  Label: string;
  Name: string;
}

/** unknown */
export interface BranchingOperationSpec {
  ConditionOperation: unknown;
  OperationsIfFailure: unknown;
  OperationsIfSuccess: unknown;
}

/** both */
export interface BuffAddedEventArgs {
  BuffModel: BuffModel;
}

/** unknown */
export interface BuffEffectSpec {
  Booleans: unknown;
}

/** both */
export interface BuffExpiredEventArgs {
  SpecContainerId: number;
}

/** request */
export interface BuffInfoPanelNavigationModel {
  HeroBuffs: unknown;
  HeroBuffTooltips: unknown;
  TargetBuffs: unknown;
  TargetBuffTooltips: unknown;
}

/** unknown */
export interface BuffItemAbilitySpec {
  BuffSpecContainerId: unknown;
}

/** unknown */
export interface BuffLabelReferenceSpec {
  Label: unknown;
}

/** both */
export interface BuffModel {
  IconUrl: string;
  IsDebuff: boolean;
  IsRatioFixed: boolean;
  LayerName: string;
  MinimumStackCountToDisplay: number;
  RemainingTimeRatio: number;
  SpecContainerId: number;
  StackCount: number;
  TileAnimationType: number;
  Tooltip: unknown;
}

/** unknown */
export interface BuffOperationSpec {
  Buff: unknown;
  Label: unknown;
}

/** unknown */
export interface BuffReferenceSpec {
  Booleans: unknown;
}

/** unknown */
export interface BuffSpec {
  BuffableGameEntityTypeMask: unknown;
  BuffEffects: unknown;
  BuffPauseCondition: unknown;
  BuffStopTriggers: unknown;
  CheckBuffableGameEntityTypeMaskOnOwner: unknown;
  CreatorMaxDistance: unknown;
  Duration: unknown;
  Flags: unknown;
  InstanceCreatorType: unknown;
  InstancesRefreshType: unknown;
  IsDispellable: unknown;
  IsHidden: unknown;
  IsLinkedToCreator: unknown;
  IsPermanent: unknown;
  IsTransmittedToSpawnedCreatures: unknown;
  MaxInstances: unknown;
  MaxInstancesPerCreator: unknown;
  RefreshInterval: unknown;
  RemoveIfCreatorAbilityEnded: unknown;
  RemoveIfCreatorDied: unknown;
}

/** unknown */
export interface BuffSpecContainer {
  Type: unknown;
}

/** unknown */
export interface BuffSpecContainerRef {
  SpecContainerReferenceId: unknown;
}

/** unknown */
export interface BuffSpecContainerReferenceSpec {
  BuffSpecContainerId: unknown;
}

/** both */
export interface BuffStopTriggers {
  OnBuffedEntityAllLifeShieldsRemoved: boolean;
  OnBuffedEntityDied: boolean;
  OnBuffedEntityLifeFilled: boolean;
  OnBuffedEntityManaDepleted: boolean;
  OnBuffedEntityStunned: boolean;
}

/** request */
export interface BuffTooltipModel {
  Duration: number;
  RemainingTime: number;
  ShouldDisplayTimeInformation: boolean;
  Type: number;
}

/** unknown */
export interface BuffUiSpec {
  IconSynergyName: unknown;
  IconUrl: unknown;
  IsRatioFixedInAttack: unknown;
  MinimumElapsedTimeBeforeVisualUpdate: unknown;
  StackCountOverride: unknown;
  TileAnimationType: unknown;
}

/** unknown */
export interface BuffableSpec {
  ImmuneToBuffCreatorGameEntityTypeMask: unknown;
  PassiveBuffs: unknown;
}

/** unknown */
export interface BuffedSelectionSpec {
  BuffSpecContainerId: unknown;
}

/** request */
export interface BuildBasicTextInfoPanelNavigationModel {
  LocalizedMessage: string;
}

/** request */
export interface BuildBuildingPanelNavigationModel {
  PanelName: number;
}

/** request */
export interface BuildCommand {
  IsCastlePublishable: boolean;
}

/** request */
export interface BuildCraftingMaterialMinePanelNavigationModel {
  CraftingMaterialMineInformationModel: CraftingMaterialMineInformationModel;
  PanelName: number;
}

/** request */
export interface BuildCreaturePanelNavigationModel {
  PanelName: number;
}

/** request */
export interface BuildDecorationPanelNavigationModel {
  PanelName: number;
}

/** request */
export interface BuildEntitiesAchievement {
  EntityType: number;
  Count: number;
}

/** both */
export interface BuildEntityEventArgs {
  ContextualActionDatas: ContextualActionData;
  GameEntityId: number;
  IsNewEntity: boolean;
  SpecContainerId: number;
  SpecContainerType: number;
}

/** unknown */
export interface BuildEntitySelectedAssignmentTriggerSpec {
  GameEntityType: unknown;
  SpecContainerId: unknown;
}

/** unknown */
export interface BuildEntitySpecializedAssignmentTriggerSpec {
  GameEntityType: unknown;
  SpecContainerId: unknown;
  SpecializationId: unknown;
}

/** unknown */
export interface BuildEntityStampStatusAssignmentTriggerSpec {
  BuildEntityStampStatusFlag: unknown;
}

/** both */
export interface BuildEntityStampStatusEventArgs {
  BuildEntityStampStatusFlag: number;
}

/** both */
export interface BuildEntityTooltipModel {
  GameEntityId: number;
  ItemTypeOasisId: number;
  Level: number;
  Name: string;
  TooltipDisplayDelay: number;
}

/** request */
export interface BuildHarvestingPanelNavigationModel {
  PanelName: number;
}

/** both */
export interface BuildHistory {
  BuildDateTime: string;
  Duration: number;
  Id: unknown;
}

/** both */
export interface BuildHistoryId {
  AccountId: number;
  Index: number;
}

/** both */
export interface BuildInfo {
  ArchitectOfficeRank: number;
  BuildingNextIndex: number;
  CastleHeartRank: number;
  CastleStats: CastleStats;
  CastleType: number;
  CreatureArchetypes: unknown;
  CreatureNextIndex: number;
  DecorationNextIndex: number;
  Draft: unknown;
  HeroCorpses: unknown;
  InventoryDecorations: InventoryDecoration;
  InventoryDefenseIngredientBoosts: InventoryDefenseIngredientBoost;
  InventoryRooms: InventoryRoom;
  InventoryThemes: number;
  IsDraftPublished: boolean;
  IsRollbackAvailable: boolean;
  Level: number;
  MineStatuses: unknown;
  OwnerSpecialPacks: number;
  RoomNextIndex: number;
  ShieldEndExpirableId: string;
  TimerDuration: number;
  TrapArchetypes: unknown;
  TrapNextIndex: number;
  TriggerNextIndex: number;
  WorkersAvailable: number;
  WorkersCabinRank: number;
}

/** request */
export interface BuildInfoUpdatedNotification {
  BuildInfo: BuildInfo;
}

/** both */
export interface BuildInteractionState {
  Enable: boolean;
  GameEntityTypeMask: number;
}

/** unknown */
export interface BuildMouseButtonsAssignmentActionSpec {
  DisabledMouseButtonMask: unknown;
}

/** both */
export interface BuildNotificationEventArgs {
  Count: number;
}

/** unknown */
export interface BuildSettings {
  AutoSaveShowDuration: unknown;
  BoostCpZoneEdgeExclusionWidth: unknown;
  BoundingRadiusExclusionFlags: unknown;
  BuildCameraInitialTargetSpecContainerId: unknown;
  BuildCameraInitialTargetSpecContainerType: unknown;
  BuildUIFeedbackInfos: unknown;
  CameraModeZoomThreshold: unknown;
  CastleBuildCommandsSendInterval: unknown;
  CastleLevelAdjustmentTable: unknown;
  CastleLevelAdjustmentTreshold: unknown;
  CastleMaxTrapPerRoom: unknown;
  CastlePendingMaxCommands: unknown;
  CastlePublishMinCastleLevel: unknown;
  CastleTrapCpValue: unknown;
  ConsoleCameraTargetPositionDamping: unknown;
  ConsolePickingCursorMaxSpeed: unknown;
  ConsolePickingCursorMinSpeed: unknown;
  ConsolePickingCursorSnappingDamping: unknown;
  ConsolePickingCursorSnappingEnabled: unknown;
  ConsolePickingCursorSnappingRadius: unknown;
  ConsolePickingCursorSnappingThreshold: unknown;
  CpZoneBaseMaxCapacity: unknown;
  CreatureHarvestingCookingTime: unknown;
  CreaturesToStamp: unknown;
  DefaultDecorationPointsCostPerFootprintSqr: unknown;
  DefaultRoomMaxDecorationPoints: unknown;
  EntityHoverTooltipDelay: unknown;
  EntityHoverTooltipPixelTolerance: unknown;
  HarvestingAutoCollectDelay: unknown;
  IgnoreCpZoneMaxCapacityForPVE: unknown;
  InvalidBuildActionsFeedbacks: unknown;
  InvalidCastleFeedbacksInfos: unknown;
  MaxBoostedCreaturePerCastleLevel: unknown;
  MinCameraZoomForRoomPicking: unknown;
  MinePartialHarvestReactivationDelay: unknown;
  NormalCpZoneEdgeInclusionWidth: unknown;
  OverlappingInclusionFlags: unknown;
  SellIGCConversionRate: unknown;
  SellPMConversionRate: unknown;
  TooltipDisplayDelay: unknown;
  TrapExclusionThickness: unknown;
  UseDynamicCpZones: unknown;
  ZoomToBuildingCameraOffsetX: unknown;
  ZoomToBuildingCameraOffsetZ: unknown;
  ZoomToBuildingDuration: unknown;
  ZoomToBuildingEaseInOut: unknown;
  GeneralSettings: unknown;
}

/** both */
export interface BuildShortcutKeyModel {
  ShortcutKey: string;
  SlotIndex: number;
}

/** both */
export interface BuildToolModeChangedEventArgs {
  BuildToolbarModel: BuildToolbarModel;
}

/** both */
export interface BuildToolModeInspectUpdatedEventArgs {
  IsActive: boolean;
}

/** unknown */
export interface BuildToolModeSelectedAssignmentTriggerSpec {
  BuildToolMode: unknown;
}

/** both */
export interface BuildToolbarModel {
  BuildToolMode: number;
  PickedUpEntityId: number;
}

/** request */
export interface BuildTotemPanelNavigationModel {
  PanelName: number;
}

/** request */
export interface BuildTrapPanelNavigationModel {
  PanelName: number;
}

/** request */
export interface BuildUIFeedbackInfos {
  AggroZoneCreatureFloatingText: unknown;
  AggroZonePowerSupplyFloatingText: unknown;
  AggroZoneTrapFloatingText: unknown;
  CreatureToTotemFloatingText: unknown;
  TotemFloatingText: unknown;
}

/** both */
export interface BuildViewModel {
  Level: number;
  Properties: unknown;
  ShieldRemainingTime: number;
}

/** unknown */
export interface BuildableSpec {
  IsInUbisoftCastleBuildInventoryOnly: unknown;
  IsNotInBuildInventory: unknown;
  IsOld: unknown;
  IsRare: unknown;
}

/** both */
export interface BuilderLevelProgression {
  Level: number;
  RandomHeroCorpseCurrencyDrops: unknown;
  RandomHeroCorpseExtraDrops: unknown;
}

/** unknown */
export interface BuildingAssignmentConditionSpec {
  BuildingSpecContainerIds: unknown;
  CheckUpgradeCompleted: unknown;
  Rank: unknown;
}

/** request */
export interface BuildingExpirable {
  BuildingId: number;
  ExpirableType: number;
  SpecContainerId: number;
}

/** request */
export interface BuildingFinishNowModel {
  BuildingName: string;
  BuildingRank: number;
}

/** request */
export interface BuildingInfoDataModel {
  CurrentAttackTicketsInBossRoom: number;
  CurrentAttackTicketsInCastle: number;
  CurrentConstructionPoints: number;
  CurrentHardCapBonusCastle: number;
  MaxAttackTicketsInBossRoom: number;
  MaxAttackTicketsInCastle: number;
  MaxConstructionPoints: number;
}

/** both */
export interface BuildingInfoModel {
  BuildingInfoDataModel: BuildingInfoDataModel;
}

/** request */
export interface BuildingInfoPanelNavigationModel {
  BuildingId: number;
}

/** both */
export interface BuildingInstanceRequirement {
  BuildingRequirementRank: number;
  BuildingRequirementSpecContainerId: number;
}

/** request */
export interface BuildingItemUpgradePanelNavigationModel {
  HeroModel: HeroModel;
  PanelName: number;
}

/** both */
export interface BuildingNavBarLinkModel {
  BuildingType: number;
  IconUrl: string;
  IsOwned: boolean;
  TooltipText: string;
}

/** both */
export interface BuildingNavBarLinkSettings {
  BuildingType: number;
  IconUrl: string;
  IsDefendLink: boolean;
  TooltipOasisId: number;
}

/** both */
export interface BuildingNavBarModel {
  AttackLinks: unknown;
  DefendLinks: unknown;
}

/** request */
export interface BuildingNavBarPanelNavigationModel {
  BuildingType: number;
}

/** response */
export interface BuildingNavBarSettings {
  Links: number;
}

/** both */
export interface BuildingPopupInfoViewModel {
  BuildingId: number;
  BuildingName: string;
  BuildingRank: number;
  ForceLockFunctionButton: boolean;
  ForceLockUpgradeButton: boolean;
  FunctionIconUrl: string;
  FunctionName: string;
  FunctionUrl: string;
  IsActive: boolean;
  IsAffordable: boolean;
  IsBuildingRequirementMet: boolean;
  IsDestroyed: boolean;
  IsHeroLevelRequirementMet: number;
  IsUpgrading: boolean;
  MaxRankReached: boolean;
  Position: unknown;
  ShieldRemainingTime: number;
  SpecialMessage: string;
  UpgradeAcceleratorCost: unknown;
  UpgradeDuration: number;
  UpgradeProgressionPercentage: number;
  UpgradeRemainingTime: number;
  UpgradeRequirementBuildingName: string;
  UpgradeRequirementBuildingRank: number;
  WalletSummaryModel: WalletSummaryModel;
}

/** request */
export interface BuildingPopupNavigationModel {
  BuildingId: number;
}

/** both */
export interface BuildingPopupPositionModel {
  Zoom: number;
}

/** both */
export interface BuildingPopupPositionRefreshedArgs {
  BuildingPopupPositionModel: BuildingPopupPositionModel;
}

/** request */
export interface BuildingRankCondition {
  Count: number;
  Rank: number;
  SpecContainerId: number;
}

/** unknown */
export interface BuildingRankSpec {
  BuildingRequirementRank: unknown;
  BuildingRequirementSpecContainerId: unknown;
  UpgradeDuration: unknown;
  AutomaticProduction: unknown;
  Capacity: unknown;
  InitialLevel: unknown;
  LevelProductionPacks: unknown;
  ProductionPeriod: unknown;
  ProductionValue: unknown;
  QualityChance: unknown;
}

/** unknown */
export interface BuildingRequirementCommunityEvent {
  CraftingBuildingRequirementSpec: unknown;
  ItemType: unknown;
  ShopBuildingRequirementSpec: unknown;
  SpecContainerId: unknown;
}

/** unknown */
export interface BuildingRequirementSpec {
  BuildingRequirementRank: unknown;
  BuildingRequirementSpecContainerId: unknown;
}

/** unknown */
export interface BuildingSpec {
  BuildingInstanceRequirements: unknown;
  BuildingType: unknown;
  HideInShop: unknown;
  NeedWorker: unknown;
  Ranks: unknown;
  ShopItemCountStrategy: unknown;
}

/** unknown */
export interface BuildingSpecContainer {
  Type: unknown;
}

/** unknown */
export interface BuildingSpecContainerRef {
  SpecContainerReferenceId: unknown;
  iner: unknown;
}

/** request */
export interface BuildingTooltipModel {
  CreationDuration: number;
  ExistingInstances: number;
  MaxBuildingRank: number;
  MaxInstances: number;
  Rank: number;
  Type: number;
}

/** unknown */
export interface BuildingUiSpec {
  FunctionIconUrl: unknown;
  FunctionNameOasisId: unknown;
  FunctionUrl: unknown;
  ShopMenuNavigation: unknown;
  SpecialMessageOasisId: unknown;
  UnlockFunctionButtonDuringUpgrade: unknown;
}

/** unknown */
export interface BuildingUpgradeCompletedAssignmentTriggerSpec {
  BuildingSpecContainerIds: unknown;
  MaxRank: unknown;
  MinRank: unknown;
}

/** both */
export interface BuildingUpgradeCompletedEventArgs {
  BuildingUpgradeInfosModel: BuildingUpgradeInfosModel;
}

/** request */
export interface BuildingUpgradeCompletedNotification {
  BuildingId: number;
  NewRank: number;
}

/** request */
export interface BuildingUpgradeConfirmationPopupPanelNavigationModel {
  BuildingId: number;
}

/** both */
export interface BuildingUpgradeInfosModel {
  BuildingId: number;
  BuildingType: number;
  BuildingUpgradeCost: number;
  BuildingUpgradeDuration: number;
  BuildingUpgradeProgressionPercentage: number;
  BuildingUpgradeRank: number;
  BuildingUpgradeRemainingTime: number;
  BuilingSpecContainerId: number;
}

/** both */
export interface BuildingUpgradeInfosRefreshedEventArgs {
  BuildingUpgradeInfosModel: BuildingUpgradeInfosModel;
}

/** both */
export interface BuildingUpgradeModel {
  BuildingPopupPositionModel: BuildingPopupPositionModel;
  BuildingUpgradeInfosModel: BuildingUpgradeInfosModel;
}

/** request */
export interface BuildingUpgradePanelNavigationModel {
  BuildingId: number;
  BuildingRequirementLock: unknown;
  BuildingType: number;
  Description: string;
  Duration: number;
  HeroRequirementLock: unknown;
  IsActive: boolean;
  IsOpalPanel: boolean;
  LayerName: string;
  MaxRank: number;
  OptionalUpgradeText: string;
  PanelName: number;
  Rank: number;
  Title: string;
  UnlockableItemsList: unknown;
  UpgradeSkus: unknown;
  UpgradeStats: unknown;
}

/** both */
export interface BuildingUpgradePopupDataModel {
  NewMaxRooms: number;
}

/** both */
export interface BuildingUpgradePopupModel {
  BuildingUpgradePopupDataModel: BuildingUpgradePopupDataModel;
}

/** both */
export interface BuildingUpgradeStartedEventArgs {
  BuildingPopupPositionModel: BuildingPopupPositionModel;
  BuildingUpgradeInfosModel: BuildingUpgradeInfosModel;
}

/** request */
export interface BuildingUpgradeStartedNotification {
  BuildingId: number;
  ExpirableId: string;
}

/** both */
export interface BuildingUpgradeTimerPositionRefreshedEventArgs {
  BuildingUpgradeModels: BuildingUpgradeModel;
}

/** both */
export interface BuildingUpgradeViewModel {
  BuildingUpgradeModels: BuildingUpgradeModel;
}

/** unknown */
export interface BuiltEntityTweakingStartedAssignmentTriggerSpec {
  GameEntityTypeMask: unknown;
}

/** unknown */
export interface BurstDamageShieldSpec {
  BuffSpecContainerId: unknown;
  HealthPercentageThreshold: unknown;
  TimerDuration: unknown;
}

/** response */
export interface BusInfos {
  AmbienceBusIds: unknown;
  MasterBusId: string;
  MusicBusIds: unknown;
  SfxBusIds: unknown;
  VoiceBusIds: unknown;
}

/** unknown */
export interface ButtonPressedAssignmentTriggerSpec {
  Buttons: unknown;
}

/** request */
export interface BuyBackAddedNotification {
  AccountBuyBackSlot: AccountBuyBackSlot;
}

/** request */
export interface BuyBackCommand {
  BuyBackId: string;
  SlotIndexes: unknown;
}

/** request */
export interface BuyBackExpirable {
  ExpirableType: number;
}

/** request */
export interface BuyBackUpdatedNotification {
  AccountBuyBackSlot: AccountBuyBackSlot;
}

/** request */
export interface BuyCommand {
  SlotIndex: number;
}

/** request */
export interface BuyConsumableCommand {
  SlotIndexes: unknown;
}

/** request */
export interface BuyHeroItemCommand {
  SlotIndex: number;
}

/** unknown */
export interface BuyItemObjective {
  ItemId: unknown;
  MinLevel: unknown;
  ShopItemTypes: unknown;
}

/** request */
export interface BuyNewTabTooltipModel {
  PriceDescription: string;
}

/** unknown */
export interface CPBuildingRankSpec {
  MaxConstructionPoints: unknown;
}

/** both */
export interface CPUInfoTracking {
  ClockFrequencyHz: number;
  CoreCount: number;
  CPUCount: number;
  HardwareThreadCount: number;
  Name: string;
}

/** unknown */
export interface CameraAssignmentActionSpec {
  Movement: unknown;
}

/** unknown */
export interface CameraMovementSpec {
  Duration: unknown;
  EaseInOut: unknown;
  End: unknown;
  Start: unknown;
}

/** unknown */
export interface CameraPositionSpec {
  IgnoreNearestZoomLevel: unknown;
  Zoom: unknown;
}

/** unknown */
export interface CameraSpecContainer {
  Type: unknown;
}

/** unknown */
export interface CameraSpecContainerRef {
  SpecContainerReferenceId: unknown;
}

/** unknown */
export interface CannonSpec {
  Operations: unknown;
  RotationSpeed: unknown;
  StopDuration: unknown;
  SearchAngleTolerance: unknown;
  SearchDistance: unknown;
}

/** unknown */
export interface CapsuleShapeSpec {
  Height: unknown;
  Radius: unknown;
}

/** request */
export interface CasteInventoryItemModel {
  CanBeSold: boolean;
  ConstructionPoints: number;
  CreatureRank: number;
  IconUrl: string;
  IsNewlyAdded: boolean;
  IsRequirementMet: boolean;
  ItemType: number;
  LayerName: string;
  Level: number;
  Name: string;
  SellPrice: unknown;
  SlotIndex: number;
  SpecContainerId: number;
  StackCount: number;
  Tooltip: unknown;
}

/** both */
export interface Castle {
  AccountDisplayName: string;
  AccountId: number;
  CreationDate: string;
  CreatureTiers: unknown;
  LayoutId: number;
  ModificationDate: string;
  OasisNameId: number;
  Rooms: unknown;
  ThemeId: number;
  TrapTiers: unknown;
}

/** unknown */
export interface CastleAddEntitiesObjective {
  CreatureIds: unknown;
  EntityType: unknown;
}

/** both */
export interface CastleAttackComment {
  AccountId: number;
  AttackId: string;
  AvatarId: number;
  Comment: unknown;
}

/** request */
export interface CastleAttackedNotification {
  AttackCount: number;
  DeathCount: number;
  DefendLogEntry: DefendLogEntry;
  HeroCorpses: unknown;
  SuccessfulAttackCount: number;
  WinRatio: number;
  WinRatioDifficulty: number;
}

/** unknown */
export interface CastleAttackedObjective {
  DeathHero: unknown;
  FriendOnly: unknown;
}

/** both */
export interface CastleBlueprintTemplate {
  Rooms: unknown;
}

/** request */
export interface CastleBoughtNotification {
  BuildInfo: BuildInfo;
  IsStartupCastle: boolean;
}

/** both */
export interface CastleBuildable {
  BoostId: number;
  RoomZoneId: number;
}

/** request */
export interface CastleBuildableCommand {
  Id: number;
  Orientation: number;
  RoomId: number;
  RoomZoneId: number;
  SpecContainerId: number;
  SpecContainerId: number;
  SpecContainerId: number;
  IsCastlePublishable: boolean;
}

/** request */
export interface CastleBuilding {
  ExpirableId: string;
  Rank: number;
}

/** both */
export interface CastleCell {
  Type: number;
  Type: number;
  Type: number;
}

/** request */
export interface CastleCompetitionPopupPanelNavigationModel {
  AttackSource: number;
  PosX: number;
  PosY: number;
  UbisoftCompetitionId: number;
}

/** unknown */
export interface CastleContainsEntitiesObjective {
  CreatureIds: unknown;
  EntityCount: unknown;
  EntityType: unknown;
}

/** request */
export interface CastleCreature {
  AggroPropagationOffsetX: number;
  AggroPropagationOffsetZ: number;
  IsSleeping: boolean;
  TotemCastleBuildableId: number;
}

/** request */
export interface CastleDPSBoostConsumableTemplate {
  IncreasedDPS: number;
}

/** request */
export interface CastleDetailsPanelNavigationModel {
  CastleInfoModel: CastleInfoModel;
}

/** both */
export interface CastleDifficultySettings {
  CastleDifficulty: number;
  LevelFrom: number;
  LevelTo: number;
}

/** unknown */
export interface CastleDraftRollbackCommand {
  ServerCommand: unknown;
}

/** request */
export interface CastleDraftRollbackCompletedNotification {
  BuildInfo: BuildInfo;
  Failure: boolean;
}

/** both */
export interface CastleExpansion {
  SpecialGroundIds: number;
  SpecialGroundIds: number;
  SpecialGroundIds: number;
}

/** both */
export interface CastleExpansionPattern {
  CastleExpansions: CastleExpansion;
  EntranceX: number;
  EntranceY: number;
  ExitX: number;
  ExitY: number;
}

/** both */
export interface CastleForSale {
  CanBePurchased: boolean;
  CastleDescriptionOasisID: number;
  CastleIconUrl: string;
  CastleModelIndex: number;
  CastleTitleOasisID: number;
  DebugName: string;
  FakePriceOasisID: number;
  IsInteractive: boolean;
  IsStartupCastle: boolean;
  MineStatuses: unknown;
  SaleId: number;
  SpawnPlotId: number;
  ThemeFilter: number;
  UbisoftCastleId: number;
}

/** both */
export interface CastleForSaleInfoSummary {
  Amount: unknown;
  CanBePurchased: boolean;
  CastleDescriptionOasisID: number;
  CastleIconUrl: string;
  CastleInfoSummary: CastleInfoSummary;
  CastleModelIndex: number;
  CastleTitleOasisID: number;
  FakePriceOasisID: number;
  IsInteractive: boolean;
  SaleId: number;
  SpawnPlotId: number;
}

/** unknown */
export interface CastleGameStateConfig {
  CastleId: unknown;
  CastleMode: unknown;
}

/** unknown */
export interface CastleGridValidAssignmentConditionSpec {
  MinSnappedEntitiesCount: unknown;
}

/** unknown */
export interface CastleGridValidityAssignmentTriggerSpec {
  MinSnappedEntitiesCount: unknown;
}

/** both */
export interface CastleGround {
  GroundType: number;
  Id: number;
  SpecContainerId: number;
  SpecContainerId: number;
  SpecContainerId: number;
}

/** both */
export interface CastleGroundGenerationRoomSettings {
  Padding: number;
  RoomHeight: number;
  RoomWidth: number;
}

/** both */
export interface CastleGroundGenerationSettings {
  AuthorizeHolesInDiagonals: boolean;
  CastleExpansionPatterns: CastleExpansionPattern;
  DefaultGrounds: number;
  EntranceRoomSettings: unknown;
  ExitRoomSettings: unknown;
  ExpandHoleChance: number;
  HolePercentage: number;
  SpecialGroundCount: number;
  SpecialGroundMinDistance: number;
}

/** request */
export interface CastleHeartBuildingInfoDataModel {
  CurrentAttackTicketsInBossRoom: number;
  CurrentAttackTicketsInCastle: number;
  CurrentConstructionPoints: number;
  CurrentHardCapBonusCastle: number;
  MaxAttackTicketsInBossRoom: number;
  MaxAttackTicketsInCastle: number;
  MaxConstructionPoints: number;
}

/** request */
export interface CastleHeartBuildingUpgradePopupDataModel {
  NewAttackTicketsInBossRoom: number;
  NewAttackTicketsInCastle: number;
  NewConstructionPoints: number;
  NewHardCapBonusCastle: number;
}

/** both */
export interface CastleHeroCorpse {
  Amounts: unknown;
  ElapsedTimeSinceDeath: number;
  EntityHarvestId: number;
  GlobalX: number;
  GlobalZ: number;
  HeroDisplayName: string;
  HeroLevel: number;
  HeroSpecContainerId: number;
  Items: unknown;
}

/** both */
export interface CastleId {
  CastleType: number;
  Id: number;
}

/** request */
export interface CastleInfo {
  AttackabilityStatus: number;
  AttackCount: number;
  AttackerStatus: number;
  AttackSource: number;
  AttackType: number;
  AverageDuration: number;
  BestHeroSpecContainerId: number;
  CastleType: number;
  CastleValidationDuration: number;
  CompletionReward: unknown;
  DefenderAccountSummary: unknown;
  DefenderActiveConsumables: unknown;
  Difficulty: number;
  FromMachineLearning: boolean;
  IsAlmostEmpty: boolean;
  IsCastleAttackable: boolean;
  IsNew: boolean;
  IsShielded: boolean;
  IsTargetedAttack: boolean;
  LastCastleRating: number;
  LastPublishedDate: string;
  LastSeenOnline: string;
  Level: number;
  PotentialLoot: PotentialLoot;
  RevengeAttackId: string;
  RoomCount: number;
  ShieldExpirationDate: string;
  Stats: unknown;
  SuccessfulAttackCount: number;
  TrophyScore: number;
  TrophyScoreVariationLose: number;
  TrophyScoreVariationReason: number;
  TrophyScoreVariationWin: number;
  VictoryConditionLevel: number;
  VictoryConditionRewardRatios: number;
}

/** both */
export interface CastleInfoModel {
  AttackerTrophyScore: number;
  BestHeroOwned: boolean;
  BestHeroSku: string;
  CastleInfo: CastleInfo;
  CrownBonuses: number;
  DefenderActiveConsumables: unknown;
  DefenderSpecialPackModel: unknown;
  GuildIconUrl: string;
  GuildLayerName: string;
  IsCastleAttackable: boolean;
  IsCastleAttackableForTargetedAttack: boolean;
  IsRegionBoss: boolean;
  SubLeagueModel: SubLeagueModel;
  TargetedAttackAvailableCount: number;
  ValidatedAttackSource: number;
  WinRatioDefaultValue: number;
  WinRatioDifficultyOasisName: string;
}

/** both */
export interface CastleInfoSummary {
  ActivationDate: string;
  AttackerStatus: number;
  AttackType: number;
  CastleHeartRank: number;
  CastleIconUrl: string;
  CastleThemeId: number;
  CastleType: number;
  DeActivationDate: string;
  DefenderAccountSummary: unknown;
  FromMachineLearning: boolean;
  IsBranded: boolean;
  IsCastleAttackable: boolean;
  IsNew: boolean;
  IsShielded: boolean;
  LastComment: unknown;
  LastPublishedDate: string;
  Level: number;
  TrophyCooldownTimer: string;
  TrophyScore: number;
  UbisoftCompetitionId: number;
  VictoryConditionLevel: number;
  WinRatioDifficulty: number;
}

/** both */
export interface CastleInventory {
  Creatures: unknown;
  Decorations: unknown;
  Rooms: unknown;
  Traps: unknown;
}

/** both */
export interface CastleInventoryAction {
  Type: number;
}

/** request */
export interface CastleInventoryAddedAction {
  Count: number;
  ItemType: number;
  SpecId: number;
  Type: number;
}

/** request */
export interface CastleInventoryChangedNotification {
  Actions: unknown;
}

/** both */
export interface CastleInventoryItem {
  AutoLevelUp: boolean;
  AvailableCount: number;
  BlueprintUnlocked: boolean;
  NewlyAdded: boolean;
  SpecContainerId: number;
}

/** both */
export interface CastleInventoryItemAddedEventArgs {
  Item: unknown;
}

/** both */
export interface CastleInventoryItemRemovedEventArgs {
  Item: unknown;
  ItemSold: boolean;
}

/** both */
export interface CastleInventoryItemTemplate {
  AvailableCount: number;
  SpecContainerId: number;
}

/** both */
export interface CastleInventoryMenuNavigationButtonModel {
  IsDisabledOnConsoleUI: boolean;
  ItemType: number;
  LayerName: string;
  OasisId: number;
  Url: string;
}

/** request */
export interface CastleInventoryPanelNavigationModel {
  CastleInventoryViewModel: unknown;
  IsOpalPanel: boolean;
  MenuNavigationButtons: unknown;
  Tab: number;
  Title: string;
}

/** both */
export interface CastleInventoryRefreshedEventArgs {
  CastleInventoryViewModel: unknown;
  Inventory: unknown;
}

/** request */
export interface CastleInventoryRemovedAction {
  Count: number;
  ItemSold: boolean;
  ItemType: number;
  SpecId: number;
}

/** both */
export interface CastleItemValue {
  DebugName: string;
  ItemCount: number;
  ItemId: number;
  ItemType: number;
  Value: number;
}

/** response */
export interface CastleItemValueSettings {
  Items: number;
}

/** both */
export interface CastleLayout {
  Height: number;
  Id: number;
  SpecialCells: unknown;
  Width: number;
}

/** both */
export interface CastleLayoutCell {
  Type: number;
  Type: number;
  Type: number;
}

/** both */
export interface CastleLevelAdjustment {
  Adjustment: number;
  CpMaxFrom: number;
  CpMaxTo: number;
  CpMaxTresholdFrom: number;
  CpMaxTresholdTo: number;
}

/** unknown */
export interface CastleLevelAssignmentConditionSpec {
  MaxLevel: unknown;
  MinLevel: unknown;
}

/** both */
export interface CastleLevelInfoModel {
  Level: number;
}

/** request */
export interface CastleLevelReachedObjectiveRequirement {
  Level: number;
}

/** unknown */
export interface CastleLevelUpAssignmentTriggerSpec {
  Level: unknown;
}

/** both */
export interface CastleLevelUpEventArgs {
  Level: number;
  OldLevel: number;
}

/** both */
export interface CastleLevelUpInfoModel {
  Level: number;
  OldLevel: number;
}

/** request */
export interface CastleLevelUpNotification {
  AccountId: number;
  Level: number;
  OldLevel: number;
}

/** both */
export interface CastleLoadConfig {
  CastleId: number;
  CastleMode: number;
  UbisoftCompetitionId: number;
}

/** unknown */
export interface CastleLoadedAssignmentTriggerSpec {
  CastleId: unknown;
}

/** both */
export interface CastleLockedByObjectiveEventArgs {
  CastleId: CastleId;
}

/** both */
export interface CastleObjectiveStatusModel {
  IsLocked: boolean;
  ObjectiveSummaryEntryModel: ObjectiveSummaryEntryModel;
}

/** both */
export interface CastleObjectiveStatusUpdatedEventArgs {
  CastleId: CastleId;
  CastleObjectiveStatusModel: CastleObjectiveStatusModel;
}

/** request */
export interface CastlePopupPanelNavigationModel {
  AttackRegionId: number;
  AttackSource: number;
  AttackType: number;
  CastleId: number;
  CastleType: number;
  IsBossCastle: boolean;
  IsOpalPanel: boolean;
  PanelName: number;
  PosX: number;
  PosY: number;
  SubLeagueModel: SubLeagueModel;
}

/** request */
export interface CastlePopupRewardsTooltipModel {
  BuffGold: number;
  BuffLifeForce: number;
  BuffXp: number;
  ChestGold: number;
  ChestLifeForce: number;
  CreaturesAndTrapsGold: number;
  CreaturesAndTrapsLifeForce: number;
  CreaturesAndTrapsXp: number;
  LeagueBonusIGC: number;
  LeagueBonusLifeForce: number;
  LeagueName: string;
  MinesIGCAmount: number;
  MinesLifeForceAmount: number;
  MinesPremiumCashAmount: number;
  TotalMinesCount: number;
  Type: number;
}

/** request */
export interface CastlePopupStarsTooltipModel {
  CrownBonuses: number;
  Type: number;
}

/** both */
export interface CastlePropertiesChangedEventArgs {
  Properties: unknown;
}

/** both */
export interface CastlePropertiesModel {
  ArchitectOfficeReadyToUpgrade: boolean;
  CanValidateCastle: boolean;
  CastleValidated: boolean;
  CastleValidationDuration: number;
  CurrentConstructionPoints: number;
  CurrentRoomCount: number;
  DelegatedCastleValidationPendingTime: number;
  IsCastlePublishEnable: boolean;
  IsCastleShareable: boolean;
  IsCastleValid: boolean;
  IsCurrentCastlePublished: boolean;
  IsDelegatedCastleValidationPending: boolean;
  IsRollbackAvailable: boolean;
  MaxConstructionPoints: number;
  MaxRoomCount: number;
  PortalReadyToUpgrade: boolean;
}

/** both */
export interface CastleRankToVisualRankIndex {
  MaxCastleRank: number;
  VisualIndex: number;
}

/** request */
export interface CastleRatedNotification {
  AttackId: string;
  CastleRating: number;
  Message: Message;
}

/** both */
export interface CastleRatingFreePrize {
  Amount: number;
  Chance: number;
  CurrencyType: number;
}

/** both */
export interface CastleRenovationCollectedMaterialModel {
  DestinationInventory: number;
  DestinationSlotId: number;
  Item: unknown;
  SourceInventory: number;
  SourceSlotId: number;
}

/** both */
export interface CastleRenovationInventorySlotModel {
  IsOwned: boolean;
  Item: unknown;
}

/** unknown */
export interface CastleRenovationLevelAssignmentConditionSpec {
  MaxCastleRenovationLevel: unknown;
  MinCastleRenovationLevel: unknown;
  iner: unknown;
}

/** unknown */
export interface CastleRenovationLevelChangedAssignmentTriggerSpec {
  CastleRenovationLevel: unknown;
}

/** both */
export interface CastleRenovationLevelChangedEventArgs {
  CastleRenovationLevel: number;
}

/** request */
export interface CastleRenovationLevelCompletedPanelNavigationModel {
  Description: string;
  IsOpalPanel: boolean;
  IsRenovationCompleted: boolean;
  LayerName: string;
  Level: number;
  LevelNameOasisId: number;
  PanelName: number;
  Title: string;
}

/** both */
export interface CastleRenovationLevelModel {
  CastleRenovationLevel: number;
  CompletionInformation: unknown;
  InventorySlotModels: unknown;
  IsCompleted: boolean;
  LevelNameOasisId: number;
  RewardNameOasisId: number;
}

/** request */
export interface CastleRenovationLevelReachedObjectiveRequirement {
  CastleRenovationLevel: number;
}

/** both */
export interface CastleRenovationMaterialsCollectedEventArgs {
  CastleRenovationLevel: number;
  CollectedMaterialModels: unknown;
}

/** both */
export interface CastleRenovationMaterialsReadyForCollectEventArgs {
  AreRequiredMaterialsInHeroInventory: boolean;
}

/** request */
export interface CastleRenovationPanelNavigationModel {
  CastleRenovationLevelModels: CastleRenovationLevelModel;
  CurrentRenovationLevel: number;
  IsOpalPanel: boolean;
  PanelName: number;
}

/** both */
export interface CastleRenovationProgressionLockModel {
  AreRequirementsMet: boolean;
  CastleRenovationLevel: number;
}

/** unknown */
export interface CastleRenovationSettings {
  CastleRenovationUpgradeDelay: unknown;
  MaterialsTakeDelay: unknown;
  PerLevelRenovationInformation: unknown;
  TakeMaterialsOpenPanelDelay: unknown;
}

/** unknown */
export interface CastleRenovationUpgradeReadyAssignmentTriggerSpec {
  NextCastleRenovationLevel: unknown;
}

/** both */
export interface CastleRenovationUpgradeReadyEventArgs {
  NextCastleRenovationLevel: number;
}

/** both */
export interface CastleRenovationVisual {
  Fx: unknown;
  VisualGroup: string;
}

/** request */
export interface CastleRoom {
  Buildings: unknown;
  Creatures: unknown;
  Decorations: unknown;
  DefenseIngredientBoosts: unknown;
  Traps: unknown;
  Triggers: unknown;
}

/** request */
export interface CastleRoomBuildable {
  BoostId: number;
  RoomZoneId: number;
}

/** request */
export interface CastleSelectionPopulatedEventArgs {
  AttackRegion: AttackRegion;
  Result: unknown;
  ResultFromCache: boolean;
  SpecialPackModels: SpecialPackModel;
}

/** unknown */
export interface CastleSettings {
  AlmostEmptyCPRatio: unknown;
  CastleDifficultyTable: unknown;
  CastleWinRatioDifficultyTable: unknown;
  DefenseIngredientsCookingTimesByLevel: unknown;
  ProceduralBuildingRestrictionsById: unknown;
  RoomCapPhysicEntityHeight: unknown;
  RoomCapPhysicEntityWidth: unknown;
  RoomConnectorNodes: unknown;
  WinRatioDefaultValue: unknown;
}

/** both */
export interface CastleStats {
  AttackCount: number;
  HeroesKilled: number;
  MaxConstructionPoints: number;
  SuccessfulAttackCount: number;
  TotalConstructionPoints: number;
  TrapCount: number;
  WinRatio: number;
  WinRatioDifficulty: number;
}

/** both */
export interface CastleSummary {
  AccountDisplayName: string;
  AccountId: number;
  AvatarId: number;
  IsPublished: boolean;
  LastPublishedDate: string;
  Level: number;
}

/** both */
export interface CastleSummaryModel {
  AvatarUrl: string;
  Castle: Castle;
}

/** both */
export interface CastleThemeInfoModel {
  CanAfford: boolean;
  Description: string;
  IconUrl: string;
  Id: number;
  IsCastlePreviewable: boolean;
  IsCastleValid: boolean;
  Name: string;
}

/** request */
export interface CastleTrap {
  BeatIndex: number;
  PowerSupplyCastleBuildableId: number;
}

/** request */
export interface CastleTrigger {
  SizeX: number;
  SizeY: number;
}

/** unknown */
export interface CastleValidationAssignmentActionSpec {
  DisableCastleValidation: unknown;
}

/** request */
export interface CastleValidationDelegationExpirable {
  ExpirableType: number;
  RefundableIGC: number;
  RefundableLifeForce: number;
  RefundablePremiunCash: number;
  Visibility: number;
}

/** request */
export interface CastleValidationIntroPanelNavigationModel {
  CastleLevel: number;
  IsOpalPanel: boolean;
  PanelName: number;
}

/** request */
export interface CastleValidationOutroPanelNavigationModel {
  CastleLevel: number;
}

/** request */
export interface CastleValidationRequestedNotification {
  RequestorAccountId: number;
  Visibility: number;
}

/** both */
export interface CastleValidityChangedEventArgs {
  CastleValidityFeedbackModel: CastleValidityFeedbackModel;
}

/** both */
export interface CastleValidityFeedbackModel {
  InvalidCastleFeedback: string;
  InvalidCastleFeedbackTitle: string;
  IsCastlePreviewable: boolean;
  IsCastleShareable: boolean;
  IsCastleValid: boolean;
}

/** request */
export interface CastleVisitPanelNavigationModel {
  CanBePurchased: boolean;
  CastleName: string;
  FakePrice: string;
  SaleId: number;
}

/** both */
export interface CastleVisitSound {
  AmbienceSound: unknown;
  CastleSaleId: number;
  Music: unknown;
}

/** both */
export interface CastleWinRatioDifficultySettings {
  OasisId: number;
  WinRatioFrom: number;
  WinRatioTo: number;
}

/** both */
export interface CastlesForSaleSelectionResult {
  CastlesForSale: unknown;
}

/** unknown */
export interface ChainSpec {
  Duration: unknown;
  ObstacleCollisionHeight: unknown;
  ObstacleCollisionMaskAll: unknown;
  ObstacleCollisionMaskAny: unknown;
  OnChainBeginningOperations: unknown;
  Operations: unknown;
  OperationsDelay: unknown;
  PositionRestrictionType: unknown;
  PropagationDelay: unknown;
  PropagationRange: unknown;
  PropagationsCount: unknown;
  ValidTargetDistance: unknown;
}

/** unknown */
export interface ChangeBuildInteractionAssignmentActionSpec {
  DeleteInteractionState: unknown;
  DropInteractionState: unknown;
  PickupInteractionState: unknown;
  RotateInteractionState: unknown;
}

/** unknown */
export interface ChangeDestructibleStateOperationSpec {
  DamageRatio: unknown;
}

/** unknown */
export interface ChangeDoorStateOperationSpec {
  DoorState: unknown;
}

/** both */
export interface ChapterLeaderboardEntry {
  AccountSummary: AccountSummary;
  Position: number;
  Score: number;
  Seconds: number;
}

/** both */
export interface ChapterLeaderboardPage {
  Leaders: unknown;
  MyEntry: unknown;
}

/** unknown */
export interface ChapterSettings {
  LeadersDisplayCount: unknown;
}

/** request */
export interface ChapterTicketRewardItem {
  TicketCount: number;
}

/** both */
export interface Character3DViewportModel {
  Height: number;
  PosX: number;
  PosY: number;
  Width: number;
}

/** unknown */
export interface CharacterSettings {
  CriticalHitPenetration: unknown;
  DieMove: unknown;
  StunResistanceLossPerSecond: unknown;
  StunResistanceMultiplier: unknown;
}

/** both */
export interface ChatInhibitionRule {
  Threshold: number;
  Timespan: number;
  Type: number;
}

/** both */
export interface ChatLanguage {
  DebugName: string;
  IconUrl: string;
  LanguageCode: string;
  OasisNameId: number;
}

/** both */
export interface ChatLanguageModel {
  DisplayName: string;
  IconUrl: string;
  LanguageCode: string;
}

/** both */
export interface ChatMessage {
  ChatMessageType: number;
  Message: string;
  MessageDateTime: string;
  PresenceStatus: number;
  ProfileSummaryModel: ProfileSummaryModel;
}

/** both */
export interface ChatNewMessageEventArgs {
  ChatRoomMessagesModel: unknown;
}

/** request */
export interface ChatPanelNavigationModel {
  ChatRoomConfigModel: ChatRoomConfigModel;
  CurrentChatRoomMessagesModel: unknown;
  OpenMinimized: boolean;
}

/** both */
export interface ChatRoom {
  ChatRoomType: number;
  CodeName: string;
  DebugName: string;
  LanguageCode: string;
  OasisNameId: number;
  RoomId: number;
}

/** both */
export interface ChatRoomConfigModel {
  ChatKeepAliveDelay: number;
  ChatLanguages: ChatLanguage;
  ChatReconnectionDelay: number;
  ChatRoomInfos: ChatRoomInfo;
  MaxMessagesCount: number;
  RoomTypes: unknown;
  SelectedLanguageCode: string;
  SelectedRoomId: number;
  SelectedRoomType: number;
}

/** both */
export interface ChatRoomInfo {
  ChatEnabled: boolean;
  RoomName: string;
}

/** both */
export interface ChatRoomInfoModel {
  RoomDisplayName: string;
  RoomId: number;
  RoomLanguage: string;
  RoomType: number;
}

/** request */
export interface ChatRoomMessageSentTracking {
  MessageSentCount: number;
  RoomId: number;
}

/** request */
export interface ChatRoomTracking {
  RoomId: number;
}

/** unknown */
export interface ChatSettings {
  AssignmentsWithChatEnabled: unknown;
  ChatDisabledMessageOasisId: unknown;
  ChatEnabled: unknown;
  ChatEnabledCountries: unknown;
  ChatKeepAliveDelay: unknown;
  ChatLanguages: unknown;
  ChatMaxReconnectionDelay: unknown;
  ChatReconnectionDelay: unknown;
  ChatRoomFullMessageOasisId: unknown;
  ChatRoomMaxMessagesCount: unknown;
  ChatRooms: unknown;
  InhibitionRules: unknown;
}

/** both */
export interface ChatUserPresenceUpdatedEventArgs {
  PresenceStatus: number;
  ProfileSummaryModel: ProfileSummaryModel;
  RichPresenceStatus: number;
  RoomId: number;
}

/** request */
export interface ChooseFirstHeroConfirmationPanelNavigationModel {
  AreAllHeroesOwned: boolean;
  HeroIconUrl: string;
  HeroOasisId: number;
  HeroOasisName: string;
  HeroSpecContainerId: number;
}

/** request */
export interface ChooseFirstHeroPanelNavigationModel {
  ExplanationText: string;
}

/** unknown */
export interface CircleAreaOperationSpec {
  Radius: unknown;
}

/** unknown */
export interface CircleFieldSpec {
  EndRadius: unknown;
  StartRadius: unknown;
}

/** unknown */
export interface CircularShape2DSpec {
  Radius: unknown;
}

/** unknown */
export interface ClampValueSpec {
  Max: unknown;
  Min: unknown;
  Value: unknown;
}

/** unknown */
export interface ClearCooldownsOperationSpec {
  AbilitySpecContainers: unknown;
  AbilityTypeFlags: unknown;
}

/** unknown */
export interface CleaveOperationSpec {
  CleaveAngle: unknown;
  IsTargetExcluded: unknown;
  MaxDistance: unknown;
  ObstacleCollisionHeight: unknown;
  ObstacleCollisionMaskAll: unknown;
  ObstacleCollisionMaskAny: unknown;
  Operations: unknown;
  Orientation: unknown;
  Position: unknown;
  TargetGameEntityTypeMask: unknown;
}

/** request */
export interface ClientCallProfilingTracking {
  Duration: number;
  PathAndQuery: string;
}

/** request */
export interface ClientIdleCommand {
  IdleTime: number;
}

/** both */
export interface ClientSettings {
  AccountCacheValidation: boolean;
  ClientTrackingSettings: ClientTrackingSettings;
  EnableDebugPanelController: boolean;
  FriendReferalUrl: string;
  MaintenanceUrl: string;
  PrimaryShopBlingsUrl: string;
  PrimaryShopNonBlingsUrl: string;
  PrimaryShopPremiumPurchaseUrl: string;
  PrimaryShopProductPageUrl: string;
  PrimaryShopUrl: string;
  ShowWelcomePage: boolean;
  WelcomePageSmallUrl: string;
  WelcomePageUrl: string;
  XmppInfo: XmppInfo;
}

/** both */
export interface ClientTrackingSettings {
  ClientIdleInterval: number;
  EnabledNavigationTrackings: unknown;
  EnableProfiling: boolean;
  GameStateTrackingInterval: number;
  GlanceViewDurationTriggerInSeconds: number;
  IdleTimeThresholds: unknown;
}

/** both */
export interface CloseMessageBoxEventArgs {
  Id: number;
}

/** request */
export interface ClosePanelAssignmentActionSpec {
  PanelName: string;
  TargetEntitySearch: unknown;
}

/** request */
export interface ClosePopupAssignmentActionSpec {
  Id: string;
}

/** both */
export interface ClosePopupEventArgs {
  Id: string;
}

/** both */
export interface CloseWebBrowserEventArgs {
  HideBlackOverlay: boolean;
}

/** response */
export interface CommunityEvent {
  DebugName: string;
  EventEndTime: number;
  EventStartTime: number;
  Id: number;
}

/** request */
export interface CommunityEventAccountTimeShiftChangedNotification {
  TimeShift: number;
}

/** response */
export interface CommunityEventBoostSettings {
  BoostCommunityEvents: number;
}

/** unknown */
export interface CommunityEventBuildingRequirementSettings {
  BuildingRequirementEvents: unknown;
}

/** both */
export interface CommunityEventEndedEventArgs {
  CommunityEvent: CommunityEvent;
}

/** unknown */
export interface CommunityEventFreeTrialSettings {
  HeroFreeTrialCommunityEvents: unknown;
  PriceReductionConditions: unknown;
}

/** request */
export interface CommunityEventGlobalTimeShiftChangedNotification {
  TimeShift: number;
}

/** unknown */
export interface CommunityEventLootSettings {
  LootCommunityEvents: unknown;
}

/** response */
export interface CommunityEventSkuSettings {
  SkuCommunityEvents: number;
}

/** both */
export interface CommunityEventStartedEventArgs {
  CommunityEvent: CommunityEvent;
}

/** both */
export interface CommunityEventTimeShiftChangedEventArgs {
  TimeShift: number;
}

/** unknown */
export interface CompareValuesBooleanSpec {
  Operator: unknown;
  Value1: unknown;
  Value2: unknown;
}

/** request */
export interface CompetitionEndedNoRewardsNewsData {
  CastleAccountSummary: unknown;
  DisplayNameOasisId: number;
  Rank: number;
  UbisoftCompetitionId: number;
}

/** request */
export interface CompetitionEndedRewardsWonNewsData {
  CastleAccountSummary: unknown;
  DisplayNameOasisId: number;
  Rank: number;
  UbisoftCompetitionId: number;
}

/** request */
export interface CompleteAssignmentCommand {
  AssignmentId: number;
}

/** unknown */
export interface CompleteBuildingObjective {
  BuildingTypes: unknown;
  Rank: unknown;
}

/** unknown */
export interface CompleteObjectiveAssignmentActionSpec {
  ObjectiveId: unknown;
}

/** both */
export interface CompletedAssignmentsChangedEventArgs {
  CompletedAssignments: number;
  LastCompletedAssignmentId: number;
}

/** unknown */
export interface CompositeBehaviorSpec {
  Children: unknown;
}

/** unknown */
export interface CompositeOperationSpec {
  Operations: unknown;
  ResultCombinationType: unknown;
  StopCondition: unknown;
}

/** unknown */
export interface ConditionAbilityIsUsedBehaviorSpec {
  AbilityIndex: unknown;
  NumberOfUsages: unknown;
}

/** unknown */
export interface ConditionAttackUserSettingsBehaviorSpec {
  MinHeroItemQualityToPickUp: unknown;
}

/** unknown */
export interface ConditionBehaviorSpec {
  IsNot: unknown;
  SpecContainerReferenceIds: unknown;
  SpecContainerType: unknown;
  Target: unknown;
}

/** unknown */
export interface ConditionFightDynamicsBehaviorSpec {
  IsAggroTargetAttackable: unknown;
}

/** unknown */
export interface ConditionHealthIsChangedBehaviorSpec {
  IsLifeReducedOnly: unknown;
}

/** unknown */
export interface ConditionHealthIsLessThanBehaviorSpec {
  Percent: unknown;
}

/** unknown */
export interface ConditionIsAbilityCastableBehaviorSpec {
  AbilityIndex: unknown;
}

/** unknown */
export interface ConditionIsFacingTargetBehaviorSpec {
  FacingAngleModifier: unknown;
  Target: unknown;
}

/** unknown */
export interface ConditionOperationSpec {
  BooleanCondition: unknown;
  OperationsIfFalse: unknown;
  OperationsIfTrue: unknown;
}

/** both */
export interface ConditionPowerUpUnlock {
  Heroes: number;
  MinItemLevel: number;
  MinItemQuality: number;
  NamedItemPowerUpLevelUnlock: NamedItemPowerUpLevelUnlock;
  PowerUpId: number;
}

/** unknown */
export interface ConditionTargetAttackRangeWithinDistanceBehaviorSpec {
  ActionLineClearCheckWidth: unknown;
  HysteresisModifier: unknown;
  NeedActionLineClear: unknown;
  RescaleTargetAttackRange: unknown;
  RescaleTargetAttackRangeMax: unknown;
  RescaleTargetAttackRangeMin: unknown;
  RescaleTargetAttackRangeNewMax: unknown;
  RescaleTargetAttackRangeNewMin: unknown;
  Target: unknown;
  UseEntitiesRadius: unknown;
}

/** unknown */
export interface ConditionTargetBooleanBehaviorSpec {
  BooleanCondition: unknown;
  Target: unknown;
}

/** unknown */
export interface ConditionTargetCreatedBuffBehaviorSpec {
  PFO: unknown;
  Buff: unknown;
  MinCount: unknown;
  Target: unknown;
}

/** unknown */
export interface ConditionTargetExistsBehaviorSpec {
  Target: unknown;
}

/** unknown */
export interface ConditionTargetIsAggroedBehaviorSpec {
  Target: unknown;
}

/** unknown */
export interface ConditionTargetIsBehaviorSpec {
  SpecContainerReferenceIds: unknown;
  SpecContainerType: unknown;
  Target: unknown;
}

/** unknown */
export interface ConditionTargetIsBuffedBehaviorSpec {
  Buff: unknown;
  Target: unknown;
}

/** unknown */
export interface ConditionTargetIsUnreachableBehaviorSpec {
  IgnoreDanger: unknown;
  MinClosestReachablePositionDistance: unknown;
  MinDistance: unknown;
  Target: unknown;
}

/** unknown */
export interface ConditionTargetLevelIsBehaviorSpec {
  MaxLevel: unknown;
  MinLevel: unknown;
  Target: unknown;
}

/** unknown */
export interface ConditionTargetTierIsBehaviorSpec {
  Target: unknown;
  Tiers: unknown;
}

/** unknown */
export interface ConditionTargetWithinDistanceBehaviorSpec {
  ActionLineClearCheckWidth: unknown;
  Distance: unknown;
  HysteresisModifier: unknown;
  NeedActionLineClear: unknown;
  Target: unknown;
  UseEntitiesRadius: unknown;
  Source: unknown;
}

/** unknown */
export interface ConditionTargetWithinDistanceOfSourceBehaviorSpec {
  Source: unknown;
}

/** unknown */
export interface ConditionValueSpec {
  Type: unknown;
  ValueIfFailure: unknown;
  ValueIfSuccess: unknown;
}

/** unknown */
export interface ConeShapeSpec {
  Angle: unknown;
  Radius: unknown;
}

/** unknown */
export interface ConstructionPointsAssignmentConditionSpec {
  MaxRatio: unknown;
  MinRatio: unknown;
}

/** unknown */
export interface ConstructionPointsAssignmentTriggerSpec {
  MaxRatio: unknown;
  MinConstructionPoints: unknown;
  MinRatio: unknown;
}

/** request */
export interface ConstructionPointsBuiltCondition {
  Count: number;
}

/** request */
export interface ConsumableActivatedNotification {
  ActiveConsumable: ActiveConsumable;
}

/** request */
export interface ConsumableActivationConfirmationPanelNavigationModel {
  IconSynergyName: string;
  IconUrl: string;
  InventorySlotIndex: number;
  IsAlreadyActive: boolean;
  Name: string;
  TemplateId: number;
}

/** request */
export interface ConsumableBuyBackSlot {
  Item: unknown;
}

/** request */
export interface ConsumableExpirable {
  CommunityEventId: number;
  ConsumableType: number;
  ExpirableType: number;
  TemplateId: number;
}

/** request */
export interface ConsumableExpiredNotification {
  ConsumableType: number;
  TemplateId: number;
  Index: number;
  NotificationType: number;
}

/** unknown */
export interface ConsumableGenerationSettings {
  ConsumableTypeNamesTable: unknown;
  ConsumableTypeTable: unknown;
}

/** unknown */
export interface ConsumableSettings {
  TemplateList: unknown;
}

/** both */
export interface ConsumableTemplate {
  BuildingRequirementRank: number;
  BuildingRequirementSpecContainerId: number;
  IsLootable: boolean;
  MaxInventoryStackCount: number;
  Name: unknown;
  Price: unknown;
  Quality: number;
  Rarity: number;
  SteamAssetSpec: SteamAssetSpec;
  SteamAssetUiSpec: SteamAssetUiSpec;
  TemplateId: number;
  Ui: unknown;
}

/** request */
export interface ConsumableTooltipModel {
  ConsumableType: number;
  DisplayRemainingTime: boolean;
  Duration: number;
  IsInAttack: boolean;
  Quality: number;
  Quantity: number;
  QuantityAvailableForAttack: number;
  RemainingTime: number;
  Type: number;
}

/** unknown */
export interface ContextBooleanSpec {
  Type: unknown;
}

/** unknown */
export interface ContextOrientationSpec {
  Context: unknown;
  Reverse: unknown;
}

/** response */
export interface ContextRoomConnectorNodeInfo {
  Angle: number;
  SynergyEntityFileName: string;
  SynergyName: string;
}

/** unknown */
export interface ContextValueSpec {
  ContextId: unknown;
}

/** unknown */
export interface ContextVectorSpec {
  Type: unknown;
}

/** both */
export interface ContextualActionData {
  ActionType: number;
  ContextualActionDataInputType: number;
}

/** both */
export interface ContextualActionSettings {
  OasisId: number;
}

/** unknown */
export interface ControlledEffectOperationSpec {
  Angle: unknown;
  CanSourceTurn: unknown;
  DestroyAtControlStopped: unknown;
  MaxRotationSpeed: unknown;
}

/** unknown */
export interface ControlledEffectTargetSpec {
  Index: unknown;
}

/** unknown */
export interface CorpseSpec {
  ActivationDelay: unknown;
  Duration: unknown;
}

/** unknown */
export interface CorrespondingValueSpec {
  CorrespondancesDictionary: unknown;
  KeyValue: unknown;
}

/** request */
export interface CountAchievement {
  CurrencyType: number;
}

/** unknown */
export interface CountObjective {
  Count: unknown;
}

/** unknown */
export interface CountPriceReductionCondition {
  Count: unknown;
}

/** request */
export interface CountdownTimerPanelNavigationModel {
  IsTestAttack: boolean;
}

/** both */
export interface Country {
  CountryISOCode: string;
  Name: unknown;
  Ui: unknown;
  ZoneCodeName: string;
}

/** both */
export interface CountryModel {
  CountryCode: string;
  IconUrl: string;
  Name: string;
  ZoneCode: string;
}

/** unknown */
export interface CountrySettings {
  AllCountriesFilter: unknown;
  AllZonesFilter: unknown;
  Countries: unknown;
  DefaultCountryIcon: unknown;
  Zones: unknown;
}

/** unknown */
export interface CraftItemSelectedAssignmentTriggerSpec {
  IsAllRequiredSlotFilled: unknown;
}

/** both */
export interface CraftTestResult {
  LevelModifierItemCount: number;
  LevelToChanceModifiersFromSettings: unknown;
  LevelToChanceModifiersTestResult: unknown;
}

/** both */
export interface CraftingMaterial {
  Id: number;
  Quantity: number;
}

/** request */
export interface CraftingMaterialCollectingModel {
  LayerName: string;
}

/** request */
export interface CraftingMaterialConsumptionModel {
  Cost: unknown;
  CraftingMaterials: CraftingMaterial;
}

/** both */
export interface CraftingMaterialInformation {
  BaseCraftingMaterialRequirement: unknown;
  HeroSpecificCraftingMaterialRequirement: unknown;
  PerLevelCraftingMaterialRequirement: unknown;
}

/** both */
export interface CraftingMaterialMineHarvestCompletedEventArgs {
  CraftingMaterials: CraftingMaterial;
}

/** both */
export interface CraftingMaterialMineInformationModel {
  CraftingMaterialMineState: number;
  CraftingMaterials: CraftingMaterial;
  RemainingTime: number;
}

/** request */
export interface CraftingMaterialMineTooltipModel {
  CraftingMaterialMineInformationModel: CraftingMaterialMineInformationModel;
  Type: number;
}

/** both */
export interface CraftingMaterialModel {
  ActualCount: number;
  HasEnoughCraftingMaterial: boolean;
  IconUrl: string;
  IsConsumed: boolean;
  LayerName: string;
  Quality: number;
  RequiredCount: number;
  TemplateId: number;
}

/** unknown */
export interface CraftingMaterialPackConsumableTemplate {
  MaterialPackId: unknown;
}

/** both */
export interface CraftingMaterialRequirement {
  Amount: number;
  TemplateId: number;
}

/** both */
export interface CraftingMaterialsPack {
  DebugName: string;
  FixedCraftingMaterials: unknown;
  FullRandomCraftingMaterialCount: number;
  Id: number;
  LayerName: string;
  OasisDescriptionId: number;
  OasisNameId: number;
  RandomCraftingMaterialsByQuality: unknown;
  RandomCraftingMaterialsByQualityList: unknown;
  ShopIconUrl: string;
  UseSmartLootCraftingPriority: boolean;
}

/** request */
export interface CraftingMaterialsPackModel {
  LayerName: string;
  SpecContainerId: number;
  Type: number;
}

/** request */
export interface CraftingMaterialsPackPurchasedNotification {
  CraftingMaterialsGained: unknown;
}

/** both */
export interface CraftingMaterialsPackResultModel {
  CraftingMaterialsGained: unknown;
}

/** unknown */
export interface CraftingMaterialsPacksSettings {
  CraftingMaterialsPacks: unknown;
  FullRandomQualityChances: unknown;
}

/** request */
export interface CraftingMaterialsRewardItem {
  CraftingMaterials: CraftingMaterial;
}

/** request */
export interface CraftingStampingCounterModel {
  UIGridItemModel: UIGridItemModel;
}

/** unknown */
export interface CreatureAiSpec {
  Behavior: unknown;
  BehaviorType: unknown;
  CheckPlayerDistanceToDoTasks: unknown;
  PrioritizeRecurringTasks: unknown;
}

/** request */
export interface CreatureBoostPanelNavigationModel {
  ActiveBoostDurationLeft: number;
  ActiveBoostTotalDuration: number;
  BoostDescription: string;
  BoostDuration: number;
  BoostLayerName: string;
  BoostName: string;
  CanAfford: boolean;
  Cost: unknown;
  CraftingMaterials: CraftingMaterial;
  CreatureName: string;
  CurrentBoostedCreatureCount: number;
  IsBoostable: boolean;
  MaxBoostedCreatureCount: number;
}

/** unknown */
export interface CreatureBoostSpec {
  Abilities: unknown;
  PassiveBuffs: unknown;
}

/** response */
export interface CreatureRankColorTableEntry {
  CreatureRank: number;
  DarkColor: number;
  LightColor: number;
}

/** unknown */
export interface CreatureSpawnOperationSpec {
  AutoLevelUp: unknown;
  Creature: unknown;
  CreatureCount: unknown;
  DistanceToSpawn: unknown;
  InheritSourceMasterOwnerAutoLevelUp: unknown;
  IsSpawnSpecApplied: unknown;
  Level: unknown;
  LifeValue: unknown;
  SpawnRestrictionType: unknown;
  Specialization: unknown;
}

/** unknown */
export interface CreatureSpec {
  BehaviorCategoryId: unknown;
  Rank: unknown;
}

/** unknown */
export interface CreatureSpecContainer {
  Type: unknown;
  SpecContainerReferenceId: unknown;
}

/** unknown */
export interface CreatureSpecContainerRef {
  SpecContainerReferenceId: unknown;
}

/** unknown */
export interface CreatureSpecializationSpec {
  Behavior: unknown;
  EffectToSpawnOnDeathId: unknown;
  TierModifiers: unknown;
}

/** unknown */
export interface CreatureStatsSpec {
  ForCollectEvent: unknown;
  AttackSpeedId: unknown;
  AttackSpeedReductionImmunity: unknown;
  BaseDamageReflection: unknown;
  BaseDodge: unknown;
  BaseFacingConeAngle: unknown;
  BaseGrip: unknown;
  BaseHealMultiplier: unknown;
  BaseHealthRegeneration: unknown;
  BaseHealthStolen: unknown;
  BaseManaStolen: unknown;
  BaseMovementReduction: unknown;
  BaseMovementSpeed: unknown;
  BasePoisonTarget: unknown;
  BaseSnareTarget: unknown;
  BaseStunDurationReduction: unknown;
  BaseStunTarget: unknown;
  BaseTrapStunDurationReduction: unknown;
  BaseTurningRate: unknown;
  DamageReduction: unknown;
  DamageReflectionPerLevel: unknown;
  DodgePerLevel: unknown;
  FacingConeAnglePerLevel: unknown;
  GripPerLevel: unknown;
  HealMultiplierPerLevel: unknown;
  HealthRegenerationPerLevel: unknown;
  HealthStolenPerLevel: unknown;
  ManaStolenPerLevel: unknown;
  MovementSpeedId: unknown;
  MovementSpeedPerLevel: unknown;
  MoveSpeedReductionImmunity: unknown;
  PoisonTargetPerLevel: unknown;
  SnareTargetPerLevel: unknown;
  StunDurationReductionPerLevel: unknown;
  StunTargetPerLevel: unknown;
  TrapStunDurationReductionPerLevel: unknown;
  TurningRatePerLevel: unknown;
}

/** unknown */
export interface CreatureTierModifierSpec {
  Abilities: unknown;
  BasicAttackSlotIndex: unknown;
  PassiveBuffs: unknown;
  StatsModifier: unknown;
  Tiers: unknown;
}

/** unknown */
export interface CreatureTiersSpec {
  Specializations: unknown;
  TemporarySpecializationRanks: unknown;
}

/** both */
export interface CreatureTrapAbilityModel {
  Description: string;
  Formulas: unknown;
  IconUrl: string;
  LayerName: string;
  Title: string;
}

/** both */
export interface CreatureTrapCraftingItemModel {
  IsBlueprintLocked: boolean;
  IsCraftable: boolean;
}

/** request */
export interface CreatureTrapLevelUpPanelNavigationModel {
  ShopCategory: number;
}

/** request */
export interface CreatureTrapPanelNavigationModel {
  CreatureTrapUpgradeModel: CreatureTrapUpgradeModel;
  SpecContainerId: number;
  Tier: number;
}

/** both */
export interface CreatureTrapSpecializationModel {
  Description: string;
  Formulas: unknown;
  IconUrl: string;
  Name: string;
  SpecializationId: number;
}

/** request */
export interface CreatureTrapSpecializationPanelNavigationModel {
  GameEntityType: number;
  PosX: number;
  PosY: number;
}

/** both */
export interface CreatureTrapSpecializationViewModel {
  CreatureTrapSpecializations: unknown;
  CurrentSpecializationId: number;
  SpecContainerId: number;
  Tier: number;
  Title: string;
}

/** request */
export interface CreatureTrapTooltipModel {
  Abilities: unknown;
  AttackSpeed: string;
  AutoLevelUp: boolean;
  BehaviorCategory: string;
  DamageFormula: string;
  DefensePoints: number;
  Health: number;
  IsOldIngredient: boolean;
  Level: number;
  MaxLevel: number;
  MovementSpeed: string;
  RequiredCraftingMaterials: unknown;
  ShopContext: number;
  ShowSpecializations: boolean;
  Specializations: unknown;
  Tier: number;
  Type: number;
}

/** both */
export interface CreatureTrapUnlockModel {
  IconUrl: string;
  Name: string;
}

/** both */
export interface CreatureTrapUpgradeModel {
  BuildingRequirementName: string;
  BuildingRequirementRank: number;
  CanAfford: boolean;
  CreatureName: string;
  CurrentEffectiveLevel: number;
  CurrentHealth: number;
  DamageFormula: string;
  EffectiveLevel: number;
  Health: number;
  IconUrl: string;
  IsBuildingRequirementMet: boolean;
  IsMaxTier: number;
  MaxEffectiveLevel: number;
  MaxHealth: number;
  NextTier: number;
  SpecContainerId: number;
  TotalUnits: number;
  Unlocks: unknown;
}

/** unknown */
export interface CreaturesSettings {
  CreatureBoostId: unknown;
  DefendingCreatureBehavior: unknown;
  DefendingSpawnCreatureBehavior: unknown;
  GlobalCreatureDamageMultiplier: unknown;
  GlobalCreatureHealthMultiplier: unknown;
  GlobalCreaturePickingShapeSizeMultiplier: unknown;
  GlobalTargetableAfterDeathTime: unknown;
  HeroAlliedCreatureBehavior: unknown;
  PetBehavior: unknown;
}

/** both */
export interface CreditsDepartmentSpecializationsSettings {
  Employees: unknown;
  SpecializationName: string;
  SpecializationNameOasisId: number;
  Specializations: unknown;
  SubSpecializations: unknown;
}

/** both */
export interface CreditsDepartmentsSettings {
  DepartmentName: string;
  DepartmentOasisId: number;
  DepartmentSubCategories: unknown;
  DepartmentSubSpecializations: unknown;
  Employees: unknown;
}

/** unknown */
export interface CreditsSettings {
  Departments: unknown;
  EmptyLinesCount: unknown;
  LegalNotice: unknown;
  OtherDepartments: unknown;
  Thanks: unknown;
}

/** both */
export interface CreditsSubSpecializationsSettings {
  Employees: unknown;
  JobName: string;
  JobNameOasisId: number;
}

/** both */
export interface CrownsDiminishingReturn {
  DeathCount: number;
  DiminishingReturnMultiplier: number;
}

/** both */
export interface CsvDataTypeInfo {
  Name: string;
  Value: number;
}

/** both */
export interface CsvEntity {
  Name: string;
  Properties: unknown;
}

/** both */
export interface CsvProperty {
  Name: string;
  Type: number;
}

/** both */
export interface CsvSchema {
  Entities: unknown;
  Types: unknown;
}

/** request */
export interface CurrencyAccumulationAchievement {
  CurrencyType: number;
}

/** both */
export interface CurrencyAmount {
  Amount: number;
  CurrencyType: number;
}

/** request */
export interface CurrencyAmountRewardItem {
  CurrencyAmount: CurrencyAmount;
  LargeIconUrl: string;
  SmallIconUrl: string;
}

/** both */
export interface CurrencySettings {
  OasisIdIGC: number;
  OasisIdLifeForce: number;
  OasisIdPremiumCash: number;
}

/** unknown */
export interface CurrentHeroAssignmentConditionSpec {
  HeroId: unknown;
}

/** unknown */
export interface CurrentHeroSpellEquippedCountAssignmentConditionSpec {
  Count: unknown;
}

/** response */
export interface CustomText {
  Items: unknown;
  LineId: number;
}

/** both */
export interface CustomTextContainer {
  Items: unknown;
}

/** unknown */
export interface CustomUiFormulaSpec {
  Formula: unknown;
  FormulaParams: unknown;
}

/** response */
export interface DamageFloatingTextOverride {
  FloatingTextByMinDamageHealthRatios: number;
}

/** response */
export interface DamageFloatingTextOverrides {
  AttackerDamageFloatingTextOverride: number;
  DefenderDamageFloatingTextOverride: number;
}

/** unknown */
export interface DamageModifierBuffEffectSpec {
  Modifier: unknown;
  UpdateModifierInterval: unknown;
}

/** unknown */
export interface DamageModifierSpec {
  Bonus: unknown;
  DamageSourceTypeFilter: unknown;
  Multiplier: unknown;
}

/** both */
export interface DamageMultiplier {
  LevelDiff: number;
  Multiplier: number;
}

/** unknown */
export interface DamageOperationSpec {
  ExtraDamageInfo: unknown;
  Value: unknown;
}

/** both */
export interface DataNavigationModel {
  HideLobbyBar: boolean;
  IsPopup: boolean;
  ShowClose: boolean;
  ShowOverlay: boolean;
}

/** both */
export interface DatabaseMigrationStatus {
  Log: string;
  Success: boolean;
}

/** unknown */
export interface DeactivateFieldOperationsOperationSpec {
  Duration: unknown;
}

/** unknown */
export interface DeactivateTrapOperationSpec {
  Duration: unknown;
  TrapEntityTypeMask: unknown;
}

/** both */
export interface DeathDetail {
  AttackFrameCount: number;
  DamageSource: number;
  DefenseIngredientId: number;
  GlobalX: number;
  GlobalZ: number;
  RoomId: number;
  RoomId: number;
  RoomId: number;
}

/** unknown */
export interface DebugCameraSpec {
  FarClip: unknown;
  FastMoveSpeed: unknown;
  Fov: unknown;
  NormalMoveSpeed: unknown;
  Pitch: unknown;
  PitchSpeed: unknown;
  RollSpeed: unknown;
  SlowMoveSpeed: unknown;
  Yaw: unknown;
  YawSpeed: unknown;
}

/** request */
export interface DebugPanelNavigationModel {
  DebugPanelName: string;
}

/** unknown */
export interface DebugPanelSettings {
  PanelNavigationModels: unknown;
}

/** request */
export interface DebugUserSettings {
  DebugFrame: number;
  LoadAtDebugFrame: boolean;
  ProceduralCastleGenerationNumberOfIterations: number;
  ProceduralCastleGenerationRuleMasks: number;
  ProtoDynamicCreatureSpawning: boolean;
  ProtoGiveXpAsLoot: boolean;
  ProtoLootFollowHero: boolean;
  ProtoLootIsPickable: boolean;
  TimeScaleCheatsFactors: number;
}

/** unknown */
export interface DecorationSpec {
  DecorationCategory: unknown;
  DecorationPointsCost: unknown;
  DecorationType: unknown;
}

/** unknown */
export interface DecorationSpecContainer {
  Type: unknown;
}

/** request */
export interface DecorationTooltipModel {
  DecorationPointsCost: number;
  DecorationType: number;
  HealthPoints: number;
  HitPoints: number;
  Type: number;
}

/** unknown */
export interface DecoratorCooldownBehaviorSpec {
  Time: unknown;
}

/** unknown */
export interface DecoratorDelayBehaviorSpec {
  MaxDelay: unknown;
  MinDelay: unknown;
}

/** unknown */
export interface DecoratorDoForBehaviorSpec {
  PHO: unknown;
  Duration: unknown;
  IsForced: unknown;
}

/** unknown */
export interface DecoratorLatchBehaviorSpec {
  Duration: unknown;
  IsResettedAtSuccess: unknown;
}

/** request */
export interface DefeatCastleAchievement {
  CastleDifficulties: unknown;
}

/** unknown */
export interface DefeatCastleObjective {
  CastleId: unknown;
  CastleTypes: unknown;
  MaxCastleLevel: unknown;
  MinCastleLevel: unknown;
}

/** request */
export interface DefeatCastleStrikeAchievement {
  IsFriend: boolean;
}

/** unknown */
export interface DefeatFriendCastleObjective {
  WithLevelAdjustment: unknown;
}

/** both */
export interface DefendLog {
  DefendLogEntries: unknown;
  OfflinePeriod: unknown;
}

/** request */
export interface DefendLogEntry {
  AttackDurationInMilliseconds: number;
  AttackerAccountSummary: unknown;
  AttackId: string;
  AttackStartDateTime: string;
  AttackType: number;
  CastleRating: number;
  CompletionType: number;
  HasReplay: boolean;
  HeroSpecContainerId: number;
  IsCastleAttackable: boolean;
  IsRevengeAttack: boolean;
  IsShielded: boolean;
  IsTargetedAttack: boolean;
  Level: number;
  Message: Message;
  PillagedMines: PillagedMine;
  PotionUsed: number;
  ResurrectionCount: number;
  RevengeEnabled: boolean;
  StolenIGC: unknown;
  StolenLifeForce: unknown;
  TrophyScoreVariation: number;
  VictoryConditionLevel: number;
  VictoryConditionRewardRatios: number;
  VictoryConditionType: number;
}

/** request */
export interface DefendLogEntryDeletedNotification {
  LastValidEntryDate: string;
}

/** both */
export interface DefendLogEntryModel {
  AvatarUrl: string;
  DefendLogEntry: DefendLogEntry;
  HeroIconModel: HeroIconModel;
  Message: string;
  SpecialPackModel: SpecialPackModel;
}

/** both */
export interface DefendLogEventArgs {
  DefendLogEntry: DefendLogEntry;
}

/** both */
export interface DefendLogModel {
  CrownBonuses: number;
  CurrentEntryModels: unknown;
  OfflineEntryModels: unknown;
  OfflineSummary: unknown;
  OlderEntryModels: unknown;
}

/** request */
export interface DefendLogSummary {
  StolenIGC: unknown;
  StolenLifeForce: unknown;
  TrophyScoreVariation: number;
}

/** both */
export interface DefendLogViewModel {
  DefendLogModel: DefendLogModel;
  TargetedAttackAvailableCount: number;
}

/** both */
export interface DefenseButtonsSettings {
  Bottom: number;
  Hovered: number;
  Idle: number;
  Pickup: number;
  Selected: number;
  Specialization: number;
}

/** request */
export interface DefenseEntityTooltipModel {
  CPCost: number;
  DefenseRating: number;
  SpecialAbilities: unknown;
  TimeToLevelUp: number;
}

/** request */
export interface DefenseHudPanelNavigationModel {
  BuildViewModel: BuildViewModel;
  IsCastleValidated: boolean;
  IsDelegatedCastleValidationPending: boolean;
}

/** both */
export interface DefenseHudSettings {
  CastleNotValidatedLayerName: string;
  CastleValidatedLayerName: string;
}

/** request */
export interface DefenseIngredientArchetype {
  Specialization: number;
  Tier: number;
}

/** request */
export interface DefenseIngredientBoostExpirable {
  BoostId: number;
  DefenseIngredientId: number;
  DefenseItemType: number;
  ExpirableType: number;
}

/** unknown */
export interface DefenseIngredientBoostSpec {
  BoostTarget: unknown;
  CraftingBuildingRequirementSpec: unknown;
  Duration: unknown;
  ShopBuildingRequirementSpec: unknown;
}

/** unknown */
export interface DefenseIngredientBoostSpecContainer {
  Type: unknown;
}

/** request */
export interface DefenseIngredientBuiltCondition {
  Count: number;
  ItemType: number;
  SpecContainerId: number;
}

/** request */
export interface DefenseIngredientDestroyedCondition {
  Count: number;
  ItemType: number;
  SpecContainerId: number;
}

/** both */
export interface DefenseIngredientLoot {
  Gold: number;
  HealthOrbFragments: number;
  Id: number;
  InventoryItems: InventoryItem;
  LifeForce: number;
  PremiumCash: number;
  Xp: number;
}

/** request */
export interface DefenseIngredientRewardItem {
  Count: number;
  ItemType: number;
  SpecId: number;
}

/** request */
export interface DefenseIngredientSparedCondition {
  ItemType: number;
  SpecContainerId: number;
}

/** both */
export interface DefenseIngredientSpecializedEventArgs {
  GameEntityType: number;
  SpecContainerId: number;
  SpecializationId: number;
}

/** both */
export interface DefenseIngredientStampingModel {
  CraftingMaterials: CraftingMaterial;
  CurrencyAmount: CurrencyAmount;
  Id: number;
  OasisNameId: number;
  RemainingStampCount: number;
}

/** unknown */
export interface DefenseIngredientStatValueUiFormulaSpec {
  StatsSpecContainerId: unknown;
  StatsSpecContainerType: unknown;
}

/** unknown */
export interface DefenseIngredientStatsSpec {
  ArmorPerLevel: unknown;
  AttackRangePerLevel: unknown;
  AttackSpeedPerLevel: unknown;
  BaseArmor: unknown;
  BaseAttackRange: unknown;
  BaseAttackSpeed: unknown;
  BaseCriticalHitChance: unknown;
  BaseCriticalHitDamageBonus: unknown;
  BaseCriticalHitResilience: unknown;
  BaseHealth: unknown;
  BasePhysicalDamage: unknown;
  CriticalHitChancePerLevel: unknown;
  CriticalHitDamageBonusPerLevel: unknown;
  CriticalHitResiliencePerLevel: unknown;
  HealthPerLevel: unknown;
  PhysicalDamagePerLevel: unknown;
}

/** both */
export interface DefenseIngredientTier {
  AutoLevelUp: boolean;
  SpecContainerId: number;
  Specialization: number;
  Tier: number;
}

/** unknown */
export interface DefenseIngredientTierSpec {
  Level: unknown;
  Tier: unknown;
}

/** unknown */
export interface DefensePointsObjective {
  CPTotal: unknown;
}

/** both */
export interface DestroyFieldTriggers {
  OnChestLocked: boolean;
  OnMaxActivationReached: boolean;
}

/** unknown */
export interface DestructibleLevelSpec {
  States: unknown;
}

/** unknown */
export interface DestructibleSpec {
  AutoRepair: unknown;
  Levels: unknown;
  RepairTime: unknown;
}

/** unknown */
export interface DestructibleStateSpec {
  DamageThreshold: unknown;
}

/** unknown */
export interface DestructibleStatsSpec {
  pIO: unknown;
  BaseHitPoints: unknown;
  HealthPerCastleLevel: unknown;
  HitPointsPerLevel: unknown;
}

/** unknown */
export interface DiceRollOperationSpec {
  Operations: unknown;
  Probability: unknown;
}

/** unknown */
export interface DiffVectorSpec {
  Value1: unknown;
  Value2: unknown;
}

/** unknown */
export interface DirectionOrientationSpec {
  Direction: unknown;
}

/** unknown */
export interface DirectionalCannonSpec {
  RotationEaseInOut: unknown;
  TravelingAngle: unknown;
}

/** unknown */
export interface DiscreteOrientationSpec {
  Orientation: unknown;
}

/** both */
export interface DiskInfoTracking {
  DriveLetter: string;
  FileSystemName: string;
  FreeSpaceBytes: number;
  TotalSpaceBytes: number;
  UsedSpaceBytes: number;
}

/** both */
export interface DisplayAdapterInfoTracking {
  DisplayMode: unknown;
  DriverDesc: string;
  GPUCount: number;
  LastSupportedDirectXVersion: string;
  Name: string;
  VRAMBytes: number;
}

/** both */
export interface DisplayModeInfoTracking {
  BitsPerPixel: number;
  Height: number;
  RefreshRate: number;
  Width: number;
}

/** unknown */
export interface DisplayNameSettings {
  AccountDisplayNameNoMatchRegex: unknown;
  ChooseDisplayNameAssignementId: unknown;
  LastSettingsUpdateDate: unknown;
}

/** unknown */
export interface DisplayObjectiveCompletedAssignmentActionSpec {
  ObjectiveId: unknown;
}

/** request */
export interface DisplayPlayerCastleInAttackSelectionAssignmentActionSpec {
  DisplayPlayerCastle: boolean;
}

/** both */
export interface DistanceFieldSettings {
  Gradient: number;
  InnerColor: number;
  InnerGradient: number;
  InnerOffsetX: number;
  InnerOffsetY: number;
  InnerSize: number;
  OuterColor: number;
  OuterGradient: number;
  OuterOffsetX: number;
  OuterOffsetY: number;
  OuterSize: number;
  Thickness: number;
}

/** both */
export interface DistanceFieldSettingsModel {
  DistanceFields: unknown;
}

/** unknown */
export interface DistanceFromPlayerSelectionSpec {
  MaxDistance: unknown;
  MinDistance: unknown;
}

/** unknown */
export interface DivValueSpec {
  Value1: unknown;
  Value2: unknown;
}

/** unknown */
export interface DoorSpec {
  CloseDuration: unknown;
  DoorOpeningDelay: unknown;
  DoorStateTriggers: unknown;
  DoorTriggerDistance: unknown;
  HasDoorTrigger: unknown;
  Height: unknown;
  IsEntranceDoor: unknown;
  IsOccludable: unknown;
  ObstacleOffset: unknown;
  ObstacleRemovalDelay: unknown;
  OpenDuration: unknown;
  Thickness: unknown;
  Width: unknown;
}

/** both */
export interface DoorStateTriggers {
  OnAfterAggroActivityEnded: number;
  OnAfterAggroActivityEndedAndTestAttackCondition: number;
  OnAggroEnded: number;
  OnAggroStarted: number;
  OnAllTotemsDeactivated: number;
  OnChestLocked: number;
  OnChestOpened: number;
  OnCreation: number;
  OnCreatureAlerted: number;
  OnNoCreaturesAlerted: number;
  OnTestAttackStarted: number;
  OnTotemActivated: number;
}

/** request */
export interface DownloadCompletedTaskTracking {
  Duration: number;
  IsFirstInstall: boolean;
}

/** request */
export interface DownloadPackageCompletedTracking {
  DownloadSize: number;
  Duration: number;
  IsSuccessful: boolean;
  PackageVersionId: unknown;
}

/** request */
export interface DownloadPackageStartedTracking {
  PackageVersionId: unknown;
  Url: string;
  VersionName: string;
}

/** request */
export interface DownloadPatcherCompletedTracking {
  DownloadSize: number;
  Duration: number;
  IsSuccessful: boolean;
  PackageVersionId: unknown;
}

/** request */
export interface DownloadPatcherStartedTracking {
  PackageVersionId: unknown;
  Url: string;
  VersionName: string;
}

/** request */
export interface DownloadStartedTaskTracking {
  IsFirstInstall: boolean;
}

/** request */
export interface DraftValidatedNotification {
  BoostedCreatures: unknown;
  BoostedTraps: unknown;
  CastleValidationDuration: number;
  DefenderAccountId: number;
  IsDraftPublished: boolean;
  IsRollbackAvailable: boolean;
  SleepingCreatures: number;
}

/** both */
export interface DropCountModifer {
  AttackerCastleLevelDiff: number;
  DropModifier: number;
}

/** both */
export interface DuplicatedSpecException {
  Spec: Spec;
  SpecContainer: SpecContainer;
}

/** both */
export interface DurationByVictoryCondition {
  BaseDuration: number;
  CPMultiplier: number;
}

/** unknown */
export interface DurationSpec {
  Duration: unknown;
}

/** unknown */
export interface DyeConsumableTemplate {
  AnimationName: unknown;
  Color: unknown;
}

/** both */
export interface DyeInfoModel {
  AnimationName: string;
  CanBeTinted: boolean;
  Color: string;
  ColorName: string;
}

/** unknown */
export interface DynamicCpZoneMemberSelectionSpec {
  MaxConstructionPoints: unknown;
  MinConstructionPoints: unknown;
}

/** unknown */
export interface DynamicCpZoneMemberSpec {
  BoostZoneAggroRadius: unknown;
  ConstructionPoints: unknown;
  CreateZoneOnSpawn: unknown;
  ZoneCapacityBoost: unknown;
  ZoneRadius: unknown;
}

/** unknown */
export interface EffectActivatorFieldSpec {
  ActivationInterval: unknown;
  ActivationOperations: unknown;
  Style: unknown;
}

/** unknown */
export interface EffectFieldSpec {
  Effect: unknown;
  EffectAngles: unknown;
  EffectFieldDistributionType: unknown;
  EffectLength: unknown;
  EffectsCount: unknown;
  EffectWidth: unknown;
  IsMineField: unknown;
  Length: unknown;
  OnlySpawnEffectsInAttack: unknown;
  OverlapFilter: unknown;
  SeparationDistance: unknown;
  Width: unknown;
  ActivationInterval: unknown;
  ActivationOperations: unknown;
  Style: unknown;
}

/** both */
export interface EffectLevelLimitation {
  ItemLevel: number;
  MaxEffectLevel: number;
  MinEffectLevel: number;
}

/** unknown */
export interface EffectOperationSpec {
  Effect: unknown;
  Movement: unknown;
  Orientation: unknown;
  Position: unknown;
  SpawnRestrictionType: unknown;
  Angle: unknown;
  CanSourceTurn: unknown;
  DestroyAtControlStopped: unknown;
  MaxRotationSpeed: unknown;
}

/** unknown */
export interface EffectSpecContainer {
  Type: unknown;
}

/** unknown */
export interface EffectSpecContainerRef {
  SpecContainerReferenceId: unknown;
}

/** request */
export interface EmoteRewardItem {
  EmoteId: number;
}

/** unknown */
export interface EmptyAbilitySlotsAssignmentConditionSpec {
  AbilitySlotsCount: unknown;
  CheckEnoughUnlockedAbilities: unknown;
}

/** unknown */
export interface EnableDisableAbilitiesOperationSpec {
  AbilitySpecContainers: unknown;
  AbilityTypeFlags: unknown;
  Enable: unknown;
}

/** unknown */
export interface EnableDisableTrapPowerStateChangeSpec {
  Enable: unknown;
}

/** request */
export interface EnableHeroLevelUpNotificationAssignmentActionSpec {
  Enable: boolean;
}

/** request */
export interface EnableHeroVoiceOverAssignmentActionSpec {
  EnableHeroVoiceOver: boolean;
}

/** unknown */
export interface EnableTrapActivatedFxOperationSpec {
  Enable: unknown;
}

/** request */
export interface EndAttackInfo {
  AttackId: string;
  BoostGold: number;
  BoostLifeForce: number;
  BoostXp: number;
  CastleRatingFreePrize: CastleRatingFreePrize;
  CastleShieldedByAttacker: boolean;
  CastleShieldedDuringAttack: boolean;
  CastleValidationDuration: number;
  CompletionReward: unknown;
  CompletionType: number;
  DailyQuestGold: number;
  DeathCount: number;
  DefenderAccountDisplayName: string;
  DefenderCastleId: number;
  DefenderCastleType: number;
  DefenderLossIGC: number;
  DefenderLossLifeForce: number;
  DefenderOasisNameId: number;
  Duration: number;
  EnterTreasureRoom: boolean;
  HeroLevel: number;
  InitialGold: number;
  InitialXp: number;
  IsCastleAttackable: boolean;
  IsCompletionRewardMissed: boolean;
  IsNewUbisoftCompetitionLeader: boolean;
  IsShielded: boolean;
  IsTutorial: boolean;
  IsUbisoftCompetitionValid: boolean;
  KillsGold: number;
  KillsLifeForce: number;
  KillsXp: number;
  LastComment: unknown;
  LeagueBonusGold: number;
  LeagueBonusLifeForce: number;
  LootTransferenceCost: number;
  MaxVictoryConditionLevel: number;
  PillagedIGCMineCount: number;
  PillagedIGCMinesAmount: number;
  PillagedLifeForceMineCount: number;
  PillagedLifeForceMinesAmount: number;
  PillagedPremiumCashMineCount: number;
  PillagedPremiumCashMinesAmount: number;
  RevengeEnabled: boolean;
  TotalGold: number;
  TotalLifeForce: number;
  TotalPremiumCash: number;
  TotalXp: number;
  TreasureRoomGold: number;
  TreasureRoomLifeForce: number;
  TreasureRoomReward: unknown;
  TreasureRoomXp: number;
  TrophyScoreVariation: unknown;
  UpdatedAccountStats: unknown;
  VictoryConditionLevel: number;
  VictoryConditionRewardRatios: number;
  VictoryConditionType: number;
}

/** unknown */
export interface EndAttackParams {
  AttackFrameCount: unknown;
  AttackFrameDuration: unknown;
  CastleRating: unknown;
  Cheated: unknown;
  CollectedTrapIds: unknown;
  CompletionType: unknown;
  ConsumableUsed: unknown;
  DeactivatedTrapIds: unknown;
  DeathDetails: unknown;
  DestroyedDecorationIds: unknown;
  DestroyedTrapIds: unknown;
  Duration: unknown;
  EndAttackMessage: unknown;
  EngineTracking: unknown;
  HitByCreatures: unknown;
  HitByTraps: unknown;
  HpLost: unknown;
  KilledCreatureIds: unknown;
  LootedGoldCreatureIds: unknown;
  LootedGoldDecorationIds: unknown;
  LootedGoldTrapIds: unknown;
  LootedHealthOrbCreatureIds: unknown;
  LootedHeroItemCreatureIds: unknown;
  LootedHeroItemDecorationIds: unknown;
  LootedHeroItemTrapIds: unknown;
  LootedLifeForceCreatureIds: unknown;
  LootedLifeForceDecorationIds: unknown;
  LootedLifeForceTrapIds: unknown;
  ManaUsed: unknown;
  MineDestroyedTimeBonusCount: unknown;
  PayToKeepLoot: unknown;
  PillagedMines: unknown;
  SpellUsed: unknown;
  TotalMinesCount: unknown;
  TreasureRoomHeroItem: unknown;
  TreasureRoomLootedGold: unknown;
  TreasureRoomLootedLifeForce: unknown;
  TreasureRoomOpenFrameCount: unknown;
  TriggeredMinesCount: unknown;
}

/** both */
export interface EndBuildParams {
  BuildHistoryIndex: number;
}

/** both */
export interface EngineSetting {
  IsEngine: boolean;
  Name: string;
  Value: string;
  Version: number;
}

/** both */
export interface EngineTracking {
  EngineTrackingAverageFps: number;
  EngineTrackingTimeBetween20and59Fps: number;
  EngineTrackingTimeGreater59Fps: number;
  EngineTrackingTimeLess20Fps: number;
}

/** both */
export interface EntitiesUIContainerParameter {
  IconOffset3D: unknown;
  SpecificZoomSettings: unknown;
  UIContainer: number;
  UseHeadNode: boolean;
  ZBias: number;
}

/** unknown */
export interface EntitiesUIContainersSettings {
  AttackSelectionCastleUIContainer: unknown;
  BuildCreatureAttackTicketsUIContainer: unknown;
  BuildForgeNotificationContainer: unknown;
  BuildForgeProgressBarContainer: unknown;
  BuildMineIGCUIContainer: unknown;
  BuildMineInactiveUIContainer: unknown;
  BuildMineRepairBuildingUIContainer: unknown;
  BuildPowerSupplyUIContainer: unknown;
  BuildTotemDefenderUIContainer: unknown;
  BuildTotemSupplyUIContainer: unknown;
  BuildTrapUIContainer: unknown;
  BuildUpgradeBuildingProgressBar: unknown;
  DefaultIconOffset3D: unknown;
  DefaultZoomSettings: unknown;
  LobbyCastleUIContainer: unknown;
  LobbyHeroUIContainer: unknown;
  PremiumHeroContainer: unknown;
  StarterCastleSelectionCastleUIContainer: unknown;
}

/** unknown */
export interface EntityBuiltAssignmentTriggerSpec {
  GameEntityTypeMask: unknown;
}

/** unknown */
export interface EntityDiedAssignmentTriggerSpec {
  GameEntityTypeMask: unknown;
  SpecContainerIds: unknown;
}

/** unknown */
export interface EntityDroppedAssignmentTriggerSpec {
  GameEntityTypeMask: unknown;
}

/** unknown */
export interface EntityLifeChangedAssignmentTriggerSpec {
  GameEntityTypeMask: unknown;
  IsLifeReducedOnly: unknown;
  Value: unknown;
}

/** unknown */
export interface EntitySpawnOperationSpec {
  SpawnableEntities: unknown;
}

/** response */
export interface EnvironmentSettings {
  EastColor: number;
  EnvironmentName: number;
  FogCenterDensity: number;
  FogColor: number;
  FogIntensity: number;
  FogRampTexture: string;
  FogThreshold: number;
  GroundColor: number;
  LightingMaterialFileName: string;
  NorthColor: number;
  SkyBoxFileName: string;
  SkyColor: number;
  SouthColor: number;
  SunMaterialFileName: string;
  SunPitch: number;
  SunYaw: number;
  WestColor: number;
}

/** unknown */
export interface EnvironmentSettingsCollection {
  Environments: unknown;
}

/** response */
export interface EnvironmentSettingsGroup {
  EnvironmentSettingsList: number;
}

/** both */
export interface EquipmentAbilityModel {
  Description: string;
  DescriptionFormatter: string;
  Prefix: string;
  Suffix: string;
  Value: number;
}

/** request */
export interface EquipmentAchievement {
  EquippedParts: unknown;
}

/** both */
export interface EquipmentCategoryDefinition {
  EffectCount: number;
  OasisIds: unknown;
}

/** response */
export interface EquipmentCategorySettings {
  EquipmentCategories: unknown;
  HeroEquipmentItemTypeIconUrls: unknown;
}

/** response */
export interface EquipmentGenerationSettings {
  GearScoreMultiplier: number;
  MagicalProperties: number;
  MagicalPropertiesLevelLimitations: number;
  MaxResistance: number;
  MinimumConditionPowerUpUnlockList: number;
  NamedItemPrimaryStatsValue: number;
  PowerUpLevelLimitations: number;
  PrimaryStatLevelAdvantage: unknown;
  PrimaryStatLevelDisadvantage: unknown;
  ResistanceRandomMinRange: number;
  WeightPerResistance: number;
}

/** both */
export interface EquipmentTemplateIds {
  BackTemplateId: number;
  Finger1TemplateId: number;
  GlovesTemplateId: number;
  HelmTemplateId: number;
  NeckTemplateId: number;
  OffhandTemplateId: number;
  ShouldersTemplateId: number;
  SuitOfArmorTemplateId: number;
  WeaponTemplateId: number;
}

/** request */
export interface EquipmentTooltipModel {
  ArchetypeStats: unknown;
  ComparedMagicalProperties: unknown;
  CompareGearScore: number;
  GearScore: number;
  GearScoreType: string;
  GenderSafeItemTypeName: string;
  HeroNameRequirement: string;
  IsComparing: boolean;
  IsComparingMagicalProperties: boolean;
  IsEquipped: boolean;
  IsItemLevelHidden: boolean;
  IsUpgraded: boolean;
  ItemCategoryType: number;
  ItemQuality: number;
  ItemType: number;
  LevelMax: number;
  MagicalProperties: unknown;
  PowerUpModel: PowerUpModel;
  ShowArchetype: boolean;
  ShowWeaponDescription: boolean;
  Type: number;
  WeaponDescription: string;
  WeaponIcon: string;
  WeaponSpecialEffect: string;
}

/** both */
export interface EquippedConsumablesViewModelEventArgs {
  EquippedItems: unknown;
}

/** both */
export interface EquippedHeroConsumableItemModel {
  AbilitySlotIndex: number;
  IconUrl: string;
  LayerName: string;
  SlotIndex: number;
  StackCount: number;
  TemplateId: number;
  Tooltip: unknown;
}

/** request */
export interface EquippedHeroItemModel {
  DyeInfoModel: DyeInfoModel;
  EquippableItemSlots: unknown;
  IconUrl: string;
  IsDefaultItem: boolean;
  IsMaxLevel: boolean;
  ItemLevel: number;
  ItemSlot: number;
  Quality: number;
  Rarity: number;
  Type: unknown;
}

/** both */
export interface EquippedSpellChangedEventArgs {
  EquippedSpellViewModel: unknown;
}

/** both */
export interface EquippedSpellModel {
  IconUrl: string;
  LayerName: string;
  Level: number;
  Name: string;
  SlotIndex: number;
  SpecContainerId: number;
  Tooltip: unknown;
}

/** both */
export interface ErrorMessageInformation {
  Id: number;
  IsContinueButtonEnabled: boolean;
  IsForumLinkEnabled: boolean;
  OasisButtonCaptionId: number;
  OasisMessageId: number;
  OasisTitleId: number;
}

/** request */
export interface ErrorMessageModel {
  AdvancedMessage: string;
  ButtonCaption: string;
  IsButtonEnabled: boolean;
  IsForumLinkEnabled: boolean;
  Message: string;
  PanelName: number;
  Title: string;
  Type: number;
}

/** both */
export interface ErrorMessageUpdatedEventArgs {
  ErrorData: unknown;
  ShouldShow: boolean;
}

/** both */
export interface ErrorResultModel {
  ErrorCode: number;
}

/** response */
export interface ErrorSettings {
  Errors: number;
  ForumLinkMainOasisId: number;
  ForumLinkSecondaryOasisId: number;
}

/** unknown */
export interface ExcludedSavedTargetsSelectionSpec {
  SavedTargetSlots: unknown;
}

/** unknown */
export interface ExcludedSpecContainersSelectionSpec {
  SpecContainerIds: unknown;
  SpecContainerType: unknown;
}

/** request */
export interface ExecuteAssignmentActionCommand {
  ActionIndex: number;
  AssignmentId: number;
}

/** both */
export interface Expirable {
  ExpirableType: number;
}

/** request */
export interface ExpirableAddedNotification {
  Expirable: Expirable;
}

/** request */
export interface ExpirableRemovedNotification {
  ExpirableId: string;
}

/** request */
export interface ExpirableUpdatedNotification {
  DueDate: string;
  DurationSeconds: number;
  ExpirableId: string;
  IsPaused: boolean;
}

/** request */
export interface ExpireExpirableCommand {
  ExpirableId: string;
  PayToForceExpiration: boolean;
}

/** both */
export interface ExtraDamageInfo {
  DamageMultiplierByTargetType: unknown;
  ExtraCriticalChance: number;
  ExtraCriticalDamage: number;
  IgnoreArmor: number;
  ReduceDodgeChance: number;
}

/** both */
export interface FacebookAccountSummary {
  AvatarUrl: string;
  FacebookName: string;
  FacebookUid: string;
}

/** both */
export interface FacebookConnectEventArgs {
  IsSuccessful: boolean;
}

/** both */
export interface FacebookLinkedAccountSummary {
  AccountId: number;
  AvatarUrl: string;
  DisplayName: string;
  FacebookName: string;
  FacebookUid: string;
  HasInvited: boolean;
  IsFriend: boolean;
}

/** both */
export interface FbAccountInformation {
  first_name: string;
  id: string;
  last_name: string;
  name: string;
}

/** both */
export interface FbGetFriends {
  data: unknown;
}

/** both */
export interface FbUserInfo {
  id: string;
  name: string;
}

/** unknown */
export interface FearOperationSpec {
  Duration: unknown;
  Position: unknown;
}

/** unknown */
export interface FieldSpec {
  AllianceFilter: unknown;
  CollisionCheckInterval: unknown;
  DestroyFieldTriggers: unknown;
  Duration: unknown;
  FieldBehaviorSpec: unknown;
  GameEntityTypeMask: unknown;
  KeepEntityOnFieldRemoval: unknown;
  OnDeactivateOperations: unknown;
  OnEnterMaxActivation: unknown;
  OnEnterOperations: unknown;
  OnExitOperations: unknown;
  OnTouchOperations: unknown;
  OnUpdateDisableOperations: unknown;
  SearchMethod: unknown;
  Selections: unknown;
  TestShapeOverlap: unknown;
  TouchedEntitiesType: unknown;
  EndRadius: unknown;
  StartRadius: unknown;
}

/** request */
export interface FightDynamics {
  BasicRoomCaps: unknown;
  BossRoomCaps: unknown;
  BossUsesHardCap: boolean;
  CanGainActivationDistance: number;
  CanLoseActivationDistance: number;
  CastleLevelBonuses: unknown;
  IgnoreCapsInUbisoftCastles: boolean;
}

/** both */
export interface FightDynamicsCaps {
  SimultaneousDefendersCPHardCap: number;
  SimultaneousDefendersCPSoftCap: number;
}

/** both */
export interface FightDynamicsCastleLevelBonus {
  Bonus: number;
  MaxCastleLevel: number;
}

/** unknown */
export interface FightDynamicsSpec {
  FightDynamicsPriority: unknown;
}

/** both */
export interface Filter {
  Matched: boolean;
  Matches: unknown;
  Replacement: string;
}

/** both */
export interface FilterModel {
  Code: string;
  IconUrl: string;
  Name: string;
}

/** both */
export interface FinishNowModel {
  BuyUrl: string;
  CanAfford: boolean;
  CurrencyAmount: CurrencyAmount;
  IconUrl: string;
  ShopCategory: number;
}

/** request */
export interface FinishNowPanelNavigationModel {
  FinishNowModel: FinishNowModel;
}

/** unknown */
export interface FixedFloatValueSpec {
  Value: unknown;
}

/** unknown */
export interface FixedOrientationSpec {
  Pitch: unknown;
  Roll: unknown;
  Yaw: unknown;
}

/** unknown */
export interface FloatModifierSpec {
  Priority: unknown;
  Bonus: unknown;
  Multiplier: unknown;
}

/** unknown */
export interface FloatValueSpec {
  SaveValueSlot: unknown;
  AbilityIndex: unknown;
}

/** response */
export interface FloatingTextByMinRatio {
  FloatingText: number;
  MinRatio: number;
}

/** response */
export interface FloatingTextSettings {
  AlphaEaseOutFactor: number;
  Color: number;
  Duration: number;
  EmitAngle: number;
  EmiterHeight: number;
  EmiterOffsetX: number;
  EmiterOffsetY: number;
  EmiterWidth: number;
  EmitSpeed: number;
  EmitSpread: number;
  EmitSpreadExclusion: number;
  EndAlpha: number;
  EndScale: number;
  FollowEntity: boolean;
  FontSettings: number;
  Gravity: number;
  OasisId: number;
  OasisIdPlural: number;
  PositionEaseOutFactor: number;
  ScaleEaseOutFactor: number;
  StartAlpha: number;
  StartScale: number;
  SynergyMaterialFileName: number;
}

/** unknown */
export interface FloorMaterialOverrideSpec {
  FloorMaterialOverride: unknown;
}

/** both */
export interface FootstepsSoundSettings {
  FloorMaterialIndexByMaterialType: unknown;
  HeroFootStepSoundsTable: unknown;
}

/** request */
export interface ForgeCollectCommand {
  HeroItemSlot: number;
  InventorySlotIndex: number;
}

/** request */
export interface ForgeConfirmationPopupPanelNavigationModel {
  AverageItemLevel: number;
  HeroItemQuality: number;
}

/** both */
export interface ForgeCookingTimerUpdatedEventArgs {
  CurrencyAmount: CurrencyAmount;
  RatioPercentage: number;
  RemainingTime: number;
}

/** request */
export interface ForgeCraftCommand {
  HeroItemSlots: unknown;
  InventorySlotIndexes: number;
  Quality: number;
  ShopSkuCode: string;
}

/** unknown */
export interface ForgeCraftingMaterialsSettings {
  HeroItemCategoryTypeConversionTable: unknown;
  StatConversionTable: unknown;
}

/** request */
export interface ForgeExpirable {
  ExpirableType: number;
  ForgeMode: number;
}

/** request */
export interface ForgeFinishNowPanelNavigationModel {
  CurrencyAmount: CurrencyAmount;
  ForgeMode: number;
  ItemQuality: number;
}

/** both */
export interface ForgeInfo {
  BuildingNotificationIconUrl: string;
  BuildingProgressBarIconUrl: string;
  ShouldShowFinishNowOption: boolean;
  TierTable: unknown;
}

/** both */
export interface ForgeInventoryTabChangedEventArgs {
  HeroInventoryPanelNavigationModel: HeroInventoryPanelNavigationModel;
}

/** request */
export interface ForgeItemCollectModel {
  IconUrl: string;
  Level: number;
  OasisName: string;
  OasisNameId: number;
  TooltipModel: TooltipModel;
}

/** request */
export interface ForgeItemCookingModel {
  CurrencyAmount: CurrencyAmount;
  ForgeMode: number;
  LevelMax: number;
  LevelMin: number;
  RemainingTime: number;
  ShouldShowFinishNowOption: boolean;
  TotalDuration: number;
}

/** request */
export interface ForgeItemReadyNotification {
  AccountForgedItem: AccountForgedItem;
  ExpirableId: string;
  ForgeMode: number;
}

/** both */
export interface ForgeItemSelectionEventArgs {
  ForgeItemSlots: unknown;
  ForgeMysteryBoxModel: ForgeMysteryBoxModel;
}

/** request */
export interface ForgeItemSelectionModel {
  Duration: number;
  ForgeMode: number;
  RequiredItemSlotCount: number;
}

/** both */
export interface ForgeItemSlotModel {
  HeroItemSlot: number;
  InventorySlotIndex: number;
}

/** both */
export interface ForgeModel {
  IconUrl: string;
  Level: number;
  OasisName: string;
  OasisNameId: number;
  TooltipModel: TooltipModel;
}

/** both */
export interface ForgeMysteryBoxItemModel {
  AddedItemForgeSoundId: number;
  ForgeSlotId: number;
  HeroInventoryItemModel: HeroInventoryItemModel;
  InventorySlotId: number;
  ItemSlotModel: unknown;
}

/** both */
export interface ForgeMysteryBoxModel {
  CraftingMaterialsRequirement: unknown;
  ForgeMode: number;
  ForgeModel: ForgeModel;
  ForgeMysteryBoxItemModel: ForgeMysteryBoxItemModel;
  ForgeSkuModel: ForgeSkuModel;
  ForgeSlotId: number;
  IsAllRequiredSlotFilled: boolean;
  LevelMax: number;
  LevelMin: number;
  SelectedItemSlotCount: number;
}

/** both */
export interface ForgeNotificationsUpdatedEventArgs {
  UpgradableItemsCount: number;
  UpgradableSlots: unknown;
}

/** request */
export interface ForgePanelNavigationModel {
  ForgeMode: number;
  ForgeModel: ForgeModel;
  ForgeState: number;
  HeroInventoryPanelNavigationModel: HeroInventoryPanelNavigationModel;
  IsForgeInventoryOpenedChangingTab: boolean;
  ShopPanelNavigationModel: ShopPanelNavigationModel;
}

/** request */
export interface ForgeQualitySelectionModel {
  ForgeMode: number;
  Options: unknown;
}

/** request */
export interface ForgeQualitySelectionOptionModel {
  BuildingRankRequirement: number;
  IsBuildingRankRequirementMet: boolean;
  ItemQuality: number;
  MaxCraftableItemCount: number;
  OasisName: string;
  OasisNameId: number;
}

/** request */
export interface ForgeReforgeCommand {
  HeroItemSlot: number;
  InventorySlotIndex: number;
  Quality: number;
  ShopSkuCode: string;
}

/** response */
export interface ForgeSettings {
  AssignmentCompletedForRegularForge: number;
  CraftTable: number;
  ForgeSpecContainerId: number;
  MaxForgeItemLevel: number;
  MinCraftQuality: unknown;
  MinReforgeQuality: unknown;
  NewPlayerExperienceForgeDuration: string;
  PremiumPurchaseForgeDuration: string;
  PropertyLevelUpChances: number;
  ReforgeTable: number;
  UpgradeTable: number;
}

/** both */
export interface ForgeSkuModel {
  CanAfford: boolean;
  Price: unknown;
  SkuCode: string;
}

/** request */
export interface ForgeStartedNotification {
  AccountForgedItem: AccountForgedItem;
}

/** unknown */
export interface ForgeStateAssignmentConditionSpec {
  ForgeStates: unknown;
}

/** both */
export interface ForgeTier {
  BuildingRankRequirement: number;
  Duration: number;
  LevelToChanceModifiers: unknown;
  OptionOasisId: number;
  RequiredItemCount: number;
  ShopConfirmationOasisId: number;
  ShopConfirmationShopIconUrl: string;
}

/** request */
export interface ForgeUpgradeCommand {
  ConsumedHeroInventory: unknown;
  HeroItemSlot: number;
  InventorySlotIndex: number;
  ShopSkuCode: string;
}

/** both */
export interface ForgedItemCount {
  AccountForgedItemCount: number;
  TotalForgedItemCount: number;
}

/** request */
export interface FreeTrialActivatedNotification {
  FreeTrialType: number;
  HeroFreeTrialInfoId: number;
}

/** unknown */
export interface FreeTrialAssignmentActionSpec {
  PNO: unknown;
  ExpirationDate: unknown;
  FreeTrialType: unknown;
  HeroSpecContainerId: unknown;
}

/** request */
export interface FreeTrialConditionCompletedNotification {
  HeroSpecContainerId: number;
  PriceReductionConditionCompletedId: number;
}

/** request */
export interface FreeTrialPanelNavigationModel {
  IconUrl: string;
  RemainingDays: number;
}

/** request */
export interface FreeWorkerPanelNavigationModel {
  BuyUrl: string;
  CurrencyAmount: CurrencyAmount;
}

/** request */
export interface FriendAvatarUpdatedNotification {
  FriendAccountId: number;
  FriendAvatarId: number;
}

/** request */
export interface FriendInviteNotification {
  Invitation: unknown;
}

/** both */
export interface FriendLeaderboardModel {
  DisplayName: string;
  FacebookLinkedAccount: unknown;
  Id: number;
  IsCurrentUser: boolean;
  Rank: number;
  TrophyScore: number;
}

/** request */
export interface FriendLeagueUpdatedNotification {
  FriendAccountId: number;
  LeagueId: number;
  SubLeagueId: number;
}

/** request */
export interface FriendNotificationsPanelNavigationModel {
  DebounceSearchValue: number;
  ShowFriendReferral: boolean;
}

/** both */
export interface FriendReferral {
  NonRegisteredAccounts: unknown;
}

/** both */
export interface FriendReward {
  Id: number;
  Name: unknown;
  RefferedFriendsCount: number;
  RequiredLevel: number;
  Reward: Reward;
}

/** request */
export interface FriendRewardGrantedNewsData {
  RequiredLevel: number;
  RequiredReferralFriends: number;
  Reward: Reward;
}

/** unknown */
export interface FriendRewardSettings {
  FriendRewards: unknown;
}

/** request */
export interface FriendTrophyScoreChangedNotification {
  FriendAccountId: number;
  TrophyScore: number;
}

/** both */
export interface FriendsLeaderboardModel {
  Leaderboard: unknown;
}

/** both */
export interface FriendsViewModel {
  CurrentAccountId: number;
  Friends: unknown;
  FriendshipInvitations: FriendshipInvitation;
  SpecialPackModels: SpecialPackModel;
  TargetedAttackAvailableCount: number;
}

/** both */
export interface FriendshipActionEventArgs {
  AccountSummary: AccountSummary;
  FriendsLeaderboard: unknown;
}

/** request */
export interface FriendshipAddedNotification {
  FriendAccountSummary: unknown;
}

/** both */
export interface FriendshipInvitation {
  CreationDate: string;
  FriendAccountId: number;
  FriendAvatarId: number;
  FriendDisplayName: string;
  HasAccepted: boolean;
  HasDeclined: boolean;
  IsCastleAttackable: boolean;
  IsInvitationOwner: boolean;
  LeagueId: number;
}

/** request */
export interface FriendshipInvitationCancelledNotification {
  FriendAccountId: number;
  Index: number;
  NotificationType: number;
}

/** request */
export interface FriendshipInvitationDeclinedNotification {
  FriendAccountId: number;
}

/** both */
export interface FriendshipInvitationEventArgs {
  FriendAccountId: number;
  FriendsLeaderboard: unknown;
  Invitation: unknown;
  InvitationsToMeCount: number;
}

/** both */
export interface FriendshipInvitationModel {
  AvatarUrl: string;
  FriendshipInvitation: FriendshipInvitation;
  IsCastleAttackableForTargetedAttack: boolean;
}

/** request */
export interface FriendshipInvitationUpdatedNotification {
  FriendshipInvitation: FriendshipInvitation;
}

/** request */
export interface FriendshipRemovedNotification {
  FriendAccountId: number;
  Index: number;
  NotificationType: number;
}

/** unknown */
export interface FxSpecContainer {
  Type: unknown;
  SpecContainerReferenceId: unknown;
}

/** unknown */
export interface FxSpecContainerRef {
  SpecContainerReferenceId: unknown;
}

/** both */
export interface GPUTimings {
  SettingsMS: number;
}

/** both */
export interface GameButtonEventArgs {
  Button: number;
}

/** unknown */
export interface GameCameraInterpolationCompletedAssignmentTriggerSpec {
  GameCameraInterpolation: unknown;
}

/** unknown */
export interface GameCameraSpec {
  AabsoluteOrbitYawIncrement: unknown;
  DefaultPitchAngle: unknown;
  DefaultRollAngle: unknown;
  DefaultYawAngle: unknown;
  EnableZoomRetargeting: unknown;
  FarClip: unknown;
  InitialZoomLevel: unknown;
  KeepPlayerModifications: unknown;
  MaxInstantZoomLevelVariation: unknown;
  MicrophoneDistanceRatio: unknown;
  OcclusionRadius: unknown;
  OrbitDuration: unknown;
  OrbitEaseOutFactor: unknown;
  ShakeAnimationCooldown: unknown;
  TargetEntityDampingFactor: unknown;
  ZoomLevels: unknown;
}

/** both */
export interface GameCameraZoomLevel {
  AttachCameraLight: boolean;
  Distance: number;
  EaseInDuration: number;
  EaseInFactor: number;
  FOV: number;
  Pitch: number;
  ShowWalls: boolean;
  TargetOffsetX: number;
  TargetOffsetY: number;
  TargetOffsetZ: number;
}

/** both */
export interface GameEngineSettings {
  EngineSettings: EngineSetting;
}

/** unknown */
export interface GameNavigatedAssignmentTriggerSpec {
  ActionName: unknown;
  ControllerName: unknown;
}

/** both */
export interface GameResizedModel {
  CurrentScreenHeight: number;
  CurrentScreenWidth: number;
  PreviousScreenHeight: number;
  PreviousScreenWidth: number;
}

/** response */
export interface GameServerConnectionConfig {
  AccountName: string;
  AccountPassword: string;
  GameServerUrl: string;
  HttpCompression: boolean;
}

/** request */
export interface GameStartTracking {
  GameClientVersion: string;
  MachineId: string;
}

/** unknown */
export interface GameStateConfig {
  GameStateType: unknown;
  IsTracked: unknown;
}

/** both */
export interface GameStateSoundPresets {
  ActivationPresets: unknown;
  DeactivationPresets: unknown;
}

/** both */
export interface GameStateSoundPresetsInfo {
  GlobalPresets: unknown;
  PresetsByHeroId: unknown;
}

/** both */
export interface GameStateSoundPresetsSettings {
  GameStateSoundPresetsInfos: GameStateSoundPresetsInfo;
}

/** request */
export interface GameStateTracking {
  GameStateId: number;
  GameStateIdleTime: number;
  GameStateTotalTime: number;
  GameStateType: number;
  NextGameStateType: number;
}

/** both */
export interface GameStates {
  AccountCreation: number;
  Attack: number;
  AttackSelection: number;
  Build: number;
  CastleVisit: number;
  Home: number;
  Patcher: number;
  Replay: number;
  StarterCastleSelection: number;
  StartMenu: number;
  UPlayLinking: number;
}

/** both */
export interface GameUrlEventArgModel {
  ActionName: string;
  ControllerName: string;
  DataNavigationInfo: unknown;
  Parameters: string;
}

/** unknown */
export interface GamepadAttackSettings {
  AutoAimOverride: unknown;
  AutoAimRange: unknown;
  GamepadCursorInitialPosition: unknown;
  GamepadCursorSpeed: unknown;
  SwitchLockedTargetAutoAim: unknown;
  SwitchLockedTargetDelay: unknown;
}

/** request */
export interface GamepadButtonContextualActionData {
  Buttons: number;
  ContextualActionDataInputType: number;
}

/** unknown */
export interface GamepadSettings {
  GamepadVibrateSynergyFileName: unknown;
  InputRepeatDelay: unknown;
  InputRepeatInverseAcceleration: unknown;
}

/** request */
export interface GamepadStickContextualActionData {
  ContextualActionDataInputType: number;
  Stick: number;
}

/** both */
export interface GameplayToolboxAppConfig {
  BranchName: string;
  CommunityEventSettingsPath: string;
  EnableDevMode: boolean;
  GameEnvironmentName: string;
  GameplaySettingsPath: string;
  GameServerUrl: string;
  HMACAccessKeyID: string;
  HMACSecret: string;
  RootSettingsPath: string;
  ShopSettingsPath: string;
  SteamAppID: number;
}

/** both */
export interface GearIcons {
  InventoryIconUrl: string;
  ShopIconUrl: string;
}

/** unknown */
export interface GeneralAttackSounds {
  AbilityActivatedSound: unknown;
  AbilityCooldownEndedSound: unknown;
  AbsorbedSound: unknown;
  AttackMusic: unknown;
  AttackReportAmbienceSound: unknown;
  AttackReportMusic: unknown;
  AttackTimerBonusSound: unknown;
  AttackTimerEndedFailSound: unknown;
  BossPveCastleAttackMusic: unknown;
  ChallengeCountDown1Sound: unknown;
  ChallengeCountDown2Sound: unknown;
  ChallengeCountDown3Sound: unknown;
  ChallengeCountDownEndSound: unknown;
  ChestLootCollectedSound: unknown;
  ChestLootDroppedSound: unknown;
  ConfusedSound: unknown;
  ConsumableDroppedSound: unknown;
  CraftingMaterialDroppedSound: unknown;
  CreatureAggroedWarningSound: unknown;
  CreatureDefendingATotemAggroedWarningSound: unknown;
  DisableHeroCriticalHealthSoundPreset: unknown;
  DodgeSound: unknown;
  EnableHeroCriticalHealthSoundPreset: unknown;
  EpicFightAttackMusic: unknown;
  EpicWinJingleSound: unknown;
  HeroDeathJingleSound: unknown;
  HeroItemDroppedSound: unknown;
  HudHeroVsHeroAnimSound: unknown;
  InvalidActionFeedbackSound: unknown;
  LevelUpSound: unknown;
  LifeShieldActivationSound: unknown;
  LifeShieldDeactivationSound: unknown;
  LootCollectedSound: unknown;
  LootDroppedCoinsSound: unknown;
  LootDroppedLifeForceSound: unknown;
  LootDroppedPremiumCashSound: unknown;
  SnaredSound: unknown;
  SpellResistSound: unknown;
  StunnedSound: unknown;
  TimerEndingCountdownSound: unknown;
  TotemLeashingActivatedSound: unknown;
  TreasureRoomMusicInTime: unknown;
  TreasureRoomMusicOutOfTime: unknown;
  VictoryConditionLevelChanged: unknown;
}

/** unknown */
export interface GeneralBuildSounds {
  AggroTweakingToolActivationSound: unknown;
  AggroTweakingToolConfirmationSound: unknown;
  AggroTweakingToolDeactivationSound: unknown;
  BuildingRepairingStartedSound: unknown;
  BuildingRepairingStoppedSound: unknown;
  BuildingUpgradeEndSound: unknown;
  BuildingUpgradeStartSound: unknown;
  BuildMusic: unknown;
  BuiltEntitiesGroupReplacedSound: unknown;
  BuiltEntityDeleteSound: unknown;
  BuiltEntityDropSound: unknown;
  BuiltEntityHarvestStartedSound: unknown;
  BuiltEntityInspectSound: unknown;
  BuiltEntityPickupSound: unknown;
  BuiltEntityRotateSound: unknown;
  BuiltEntitySelectionSound: unknown;
  BuiltEntitySnapSound: unknown;
  HarvestCollectedCratingMaterialSound: unknown;
  HarvestCollectedGoldSound: unknown;
  HarvestCollectedLifeForceSound: unknown;
  HarvestCollectedPremiumCashSound: unknown;
  HarvestDroppedCraftingMaterialSound: unknown;
  HarvestDroppedGoldSound: unknown;
  HarvestDroppedLifeForceSound: unknown;
  HarvestDroppedPremiumCashSound: unknown;
  InvalidActionFeedbackSound: unknown;
  PowerInvalidConnectionBeamStartSound: unknown;
  PowerInvalidConnectionBeamStopSound: unknown;
  PowerValidConnectionBeamStartSound: unknown;
  PowerValidConnectionBeamStopSound: unknown;
  TotemDefenderLinkingSound: unknown;
  TotemDefenderUnlinkingSound: unknown;
  TotemDefenderValidLinkStartSound: unknown;
  TotemDefenderValidLinkStopSound: unknown;
  TotemInvalidConnectionBeamStartSound: unknown;
  TotemInvalidConnectionBeamStopSound: unknown;
  TotemValidConnectionBeamStartSound: unknown;
  TotemValidConnectionBeamStopSound: unknown;
  TrapPoweringSound: unknown;
  TrapUnpoweringSound: unknown;
}

/** unknown */
export interface GeneralLobbySounds {
  AttackRegionUnlockAnimationSound: unknown;
  AttackSelectionCastleHoveredSound: unknown;
  CastleSelectedSound: unknown;
  CastleSelectionAmbienceSound: unknown;
  CastleSelectionMusic: unknown;
  CastleUnSelectedSound: unknown;
  CastleVisitSounds: unknown;
  HomeAttackSelectionAmbienceSound: unknown;
  LobbyMusic: unknown;
  RegionSelectionAmbienceSound: unknown;
  WebBrowserActivationPresets: unknown;
  WebBrowserDeactivationPresets: unknown;
  Description: unknown;
}

/** unknown */
export interface GeneralSettings {
  CraftingMaterialsPacks: unknown;
  FullRandomQualityChances: unknown;
}

/** unknown */
export interface GenerateProceduralCastleAssignmentActionSpec {
  CastleGenerationNumberOfIterations: unknown;
  CastleGenerationRuleMasks: unknown;
}

/** unknown */
export interface GenericSounds {
  BoostActivatedSound: unknown;
  CameraRotationSound: unknown;
  CreditsMusic: unknown;
  DefaultCastleExteriorAmbienceSound: unknown;
  DefaultRoomAmbienceSound: unknown;
  DyeAppliedSound: unknown;
  SellInventoryItemSound: unknown;
  TrashInventoryItemSound: unknown;
  Description: unknown;
}

/** both */
export interface GetBuffsViewModel {
  Buffs: unknown;
}

/** both */
export interface GetBuildShortcutKeysModel {
  BuildShortcutKeyModels: BuildShortcutKeyModel;
}

/** both */
export interface GetCastleInventoryViewModel {
  Inventory: unknown;
}

/** both */
export interface GetCategoryConfigViewModel {
  Filters: Filter;
}

/** both */
export interface GetChatRoomMessagesModel {
  ChatRoomInfo: ChatRoomInfo;
  ChatRoomMessages: unknown;
}

/** both */
export interface GetEquippedConsumablesViewModel {
  EquippedItems: unknown;
}

/** both */
export interface GetEquippedItemsViewModel {
  Equipment: unknown;
}

/** both */
export interface GetEquippedSpellViewModel {
  EquippedSpells: unknown;
}

/** both */
export interface GetHeroInventoryEventArgs {
  GetHeroInventoryViewModel: GetHeroInventoryViewModel;
}

/** both */
export interface GetHeroInventoryViewModel {
  CanBuyNewInventoryTab: boolean;
  CurrentDisplayedInventory: unknown;
  CurrentTabIndex: number;
  InventoryTabs: unknown;
  MaxSlotCount: number;
  Price: unknown;
}

/** both */
export interface GetHeroStatsModel {
  HeroLevel: number;
  HeroName: string;
  HeroStatsModel: HeroStatsModel;
}

/** both */
export interface GetMoreCastlesButtonUpdatedEventArgs {
  CanAfford: boolean;
}

/** both */
export interface GetNewsViewModel {
  CurrentAccountId: number;
  News: News;
}

/** both */
export interface GetProductsViewModel {
  Products: unknown;
}

/** both */
export interface GetSelectedAttackRegionViewModel {
  AttackRegionId: number;
  HasPendingUpdateRegionStatus: boolean;
}

/** both */
export interface GetSpellFamiliesViewModel {
  Families: unknown;
}

/** both */
export interface GetSpellShortcutKeysModel {
  SpellShortcutKeyModels: SpellShortcutKeyModel;
}

/** both */
export interface GetSpellsViewModel {
  Spells: Spell;
}

/** both */
export interface GetUbisoftCompetitionViewModel {
  UbisoftCompetitionInfo: UbisoftCompetitionInfo;
}

/** both */
export interface GiveGiftResult {
  InvalidAccounts: number;
  ProcessedAccounts: number;
}

/** both */
export interface GlobalNotification {
  StartDate: string;
}

/** unknown */
export interface GlobalOperationSpec {
  AllianceFilter: unknown;
  Operations: unknown;
}

/** unknown */
export interface GoToScreenAssignmentActionSpec {
  GameUrl: unknown;
}

/** unknown */
export interface GoldBoostCommunityEvent {
  AttackIncreasedGold: unknown;
  MineIncreasedGold: unknown;
}

/** request */
export interface GoldBoostConsumableTemplate {
  AttackIncreasedGold: number;
  MineIncreasedGold: number;
}

/** unknown */
export interface GoldPathSpec {
  DropLocationsAlongLengthCount: unknown;
  DropLocationsAlongWidthCount: unknown;
  Length: unknown;
  MaximumDropValue: unknown;
  TotalAmount: unknown;
  Width: unknown;
}

/** unknown */
export interface GrantPrivilegesAssignmentActionSpec {
  AccountPrivileges: unknown;
}

/** both */
export interface GraphicsInfoTracking {
  CurrentDirectXVersionLetter: string;
  CurrentDirectXVersionMajor: number;
  CurrentDirectXVersionMinor: number;
  DisplayAdapters: unknown;
  ScreenCount: number;
}

/** unknown */
export interface GridMemberSpec {
  BuildXp: unknown;
  IsEditable: unknown;
  IsUserOrientable: unknown;
  KeepWorldOrientation: unknown;
}

/** both */
export interface GroupsByRank {
  Groups: number;
}

/** unknown */
export interface GuidedMoveSpec {
  ArrivalOffset: unknown;
  CollisionDistance: unknown;
  Distance: unknown;
  ExecuteOperationOnArrival: unknown;
  MovementTarget: unknown;
  Orientation: unknown;
  Speed: unknown;
  StopWhenDistanceReached: unknown;
}

/** both */
export interface Guild {
  Description: unknown;
  DisplayName: string;
  Emblem: unknown;
  Id: number;
  InviteRequests: unknown;
  JoinRequests: unknown;
  LanguageCode: string;
  Members: unknown;
  PendingValidationCastleIds: number;
  Rank: number;
  RecruitmentMode: number;
  Stats: unknown;
  TrophyScore: number;
  WelcomeMessage: unknown;
}

/** both */
export interface GuildAcceptJoinRequestStatus {
  AccountId: number;
  IsSuccess: boolean;
}

/** both */
export interface GuildBattleLog {
  BattleLogEntries: unknown;
}

/** both */
export interface GuildBattleLogModel {
  BattleLogEntries: unknown;
  LastConnectionTime: string;
}

/** both */
export interface GuildBattleLogModelRefreshedEventArgs {
  Model: unknown;
}

/** both */
export interface GuildEmblem {
  Id: number;
}

/** both */
export interface GuildHeader {
  DisplayName: string;
  Emblem: unknown;
  Id: number;
}

/** both */
export interface GuildHeaderModel {
  GuildHeader: GuildHeader;
  IconName: string;
}

/** request */
export interface GuildInfoPopupPanelNavigationModel {
  GuildId: number;
  IsOpalPanel: boolean;
  PanelName: number;
  SelectedTab: number;
}

/** both */
export interface GuildInvitation {
  CreationDate: string;
  GuildSummary: GuildSummary;
}

/** request */
export interface GuildInvitationReceivedNotification {
  GuildInvitation: GuildInvitation;
}

/** request */
export interface GuildInvitationRemovedNotification {
  AccountId: number;
  GuildId: number;
}

/** request */
export interface GuildJoinRequestAddedNotification {
  GuildId: number;
}

/** request */
export interface GuildJoinRequestReceivedNotification {
  Requestor: unknown;
}

/** request */
export interface GuildJoinRequestRemovedNotification {
  AccountId: number;
  GuildId: number;
}

/** both */
export interface GuildJoinedEventArgs {
  GuildId: number;
}

/** both */
export interface GuildLeaderboardEntry {
  GuildSummary: GuildSummary;
  Score: number;
  Seconds: number;
}

/** both */
export interface GuildLeaderboardPage {
  CurrentGuild: unknown;
  Entries: unknown;
  FirstEntryRank: number;
  Leaders: unknown;
  RemainingTime: number;
  TotalCount: number;
}

/** both */
export interface GuildLeftEventArgs {
  GuildId: number;
  GuildStillExists: boolean;
}

/** request */
export interface GuildLeftNotification {
  GuildId: number;
  GuildStillExists: boolean;
}

/** both */
export interface GuildListingItemModel {
  CanAcceptInvitation: boolean;
  GuildSummary: GuildSummary;
  IsInvitation: boolean;
  MaxMemberCount: number;
  Rank: number;
  SeparatorOasisId: number;
}

/** both */
export interface GuildListingModel {
  CanCreateGuild: boolean;
  CanScrollDown: boolean;
  CanScrollUp: boolean;
  Items: unknown;
  PageIndex: number;
}

/** both */
export interface GuildListingModelRefreshedEventArgs {
  Model: unknown;
}

/** request */
export interface GuildManagementPanelNavigationModel {
  IsOpalPanel: boolean;
  Model: unknown;
  PanelName: number;
}

/** both */
export interface GuildMember {
  AccountSummary: AccountSummary;
  JoinDate: string;
  Title: number;
}

/** request */
export interface GuildMemberJoinedNotification {
  Guild: Guild;
  JoinerId: number;
}

/** request */
export interface GuildMemberLeftNotification {
  Guild: Guild;
  Index: number;
  NotificationType: number;
}

/** both */
export interface GuildMemberModel {
  AccountSummary: AccountSummary;
  AvatarLayerName: string;
  CanAttackAsTargetAttack: boolean;
  CanAttackAsTestAttack: boolean;
  CanAttackAsValidation: boolean;
  CanRemoveMember: boolean;
  CanVisitCastle: boolean;
  ShowAttackAsTargetAttack: boolean;
}

/** request */
export interface GuildMemberTitleUpdatedNotification {
  AccountId: number;
  GuildId: number;
  Title: number;
}

/** request */
export interface GuildMemberTrophyScoreChangedNotification {
  GuildRank: number;
  GuildTrophyScore: number;
  MemberAccountId: number;
  MemberTrophyScore: number;
}

/** both */
export interface GuildNotificationCountUpdatedEventArgs {
  Count: number;
  InviteCount: number;
  NewBattleLogEntriesCount: number;
  RequestCount: number;
  ValidationRequestCount: number;
}

/** both */
export interface GuildProfileModel {
  CanEdit: boolean;
  CanLeave: boolean;
  CanRequestJoin: boolean;
  Description: string;
  DisplayName: string;
  Emblem: unknown;
  HasPendingInvitation: boolean;
  HasPendingJoinRequest: boolean;
  Id: number;
  IsGuildFull: boolean;
  JoinRequests: unknown;
  LanguageCode: string;
  LeaderDisplayName: string;
  MaxMemberCount: number;
  MemberCount: number;
  Members: unknown;
  Rank: number;
  RecruitmentMode: number;
  TrophyScore: number;
  WelcomeMessage: string;
}

/** both */
export interface GuildProfileModelRefreshedEventArgs {
  Model: unknown;
}

/** request */
export interface GuildProfilePanelNavigationModel {
  GuildId: number;
  IsOpalPanel: boolean;
  PanelName: number;
  SelectedTab: number;
}

/** both */
export interface GuildSearchResult {
  GuildSummaries: unknown;
  HasMore: boolean;
}

/** response */
export interface GuildSettings {
  AvengeeCrownsRatioOnRevenge: number;
  EntryTimeToLive: string;
  GiveRewardJobDelay: string;
  GlobalLockTimeout: string;
  GuildLeaderRewards: number;
  Languages: unknown;
  LeaderDisplayedCount: number;
  MaxBattleLogEntries: number;
  MaxEntriesPerRequest: number;
  MaxMembers: number;
  Period: string;
  ReferenceDate: number;
}

/** request */
export interface GuildSettingsUpdatedNotification {
  Description: unknown;
  GuildEmblem: GuildEmblem;
  GuildId: number;
  LanguageCode: string;
  RecruitmentMode: number;
}

/** both */
export interface GuildSummary {
  DisplayName: string;
  Emblem: unknown;
  Id: number;
  LanguageCode: string;
  LeaderAccountId: number;
  LeaderDisplayName: string;
  MemberCount: number;
  TrophyScore: number;
}

/** request */
export interface GuildWelcomePagePanelNavigationModel {
  ExcludeModalPopupOpening: boolean;
  GuildProfileModel: GuildProfileModel;
  IsOpalPanel: boolean;
  PanelName: number;
}

/** both */
export interface HMACDictionaryItem {
  AccessKeyID: string;
  Description: string;
  Secret: string;
}

/** request */
export interface HarvestCollectedEventArgs {
  AmountCollected: unknown;
  CastleLevel: number;
  EntityHarvestId: number;
  EntityHarvestType: number;
  XpEarned: number;
}

/** both */
export interface HarvestCollectingStartedEventArgs {
  CurrencyType: number;
  EntityHarvestId: number;
  EntityHarvestType: number;
}

/** request */
export interface HarvestCommandCompletedEventArgs {
  AmountCollected: unknown;
  CastleLevel: number;
  EntityHarvestId: number;
  EntityHarvestType: number;
  HarvestedHeroItems: unknown;
  XpEarned: number;
}

/** request */
export interface HarvestHeroCorpseCommand {
  HeroCorpseId: number;
  SlotsUpdates: unknown;
}

/** request */
export interface HarvestHoverModel {
  AmountToCollect: unknown;
  EntityHarvestId: number;
  EntityHarvestType: number;
  IsCookingReady: boolean;
  Position: unknown;
  RemainingTime: number;
  Xp: number;
}

/** both */
export interface HarvestListEntity {
  HarvestRefreshPositions: HarvestRefreshPosition;
}

/** request */
export interface HarvestMineBuildingCommand {
  CurrencyType: number;
  MineBuildingId: number;
}

/** both */
export interface HarvestMineStatusAddedEventArgs {
  CurrencyType: number;
  EntityHarvestId: number;
  EntityHarvestType: number;
}

/** both */
export interface HarvestOutEventArgs {
  EntityHarvestId: number;
  EntityHarvestType: number;
  IsCookingReady: boolean;
}

/** both */
export interface HarvestPositionModel {
  MaxIconSize: number;
  MaxZoom: number;
  MinIconSize: number;
  MinZoom: number;
  MinZoom: number;
  MinZoom: number;
  Zoom: number;
}

/** both */
export interface HarvestReadyForCollectEventArgs {
  HarvestHoverModel: HarvestHoverModel;
}

/** both */
export interface HarvestRefreshPosition {
  CurrencyType: number;
  EntityHarvestId: number;
  EntityHarvestType: number;
  Position: unknown;
}

/** both */
export interface HarvestRefreshedEventArgs {
  EntitiesReadyToCollect: unknown;
}

/** both */
export interface HarvestRemovedEventArgs {
  EntityHarvestId: number;
  EntityHarvestType: number;
  IsCookingReady: boolean;
}

/** both */
export interface HarvestResult {
  EntityHarvestId: number;
  EntityHarvestType: number;
  HarvestedAmount: unknown;
  HarvestedHeroItems: unknown;
  RemainingTime: number;
  ResultCode: number;
}

/** both */
export interface HarvestViewModel {
  HeroCorpsesReadyToCollect: unknown;
  MinesReadyToCollect: unknown;
}

/** request */
export interface HarvestingCompletedNotification {
  Result: unknown;
  Index: number;
  NotificationType: number;
}

/** unknown */
export interface HealOperationSpec {
  CanResurrect: unknown;
  IgnoreHealMultiplier: unknown;
  IsValueRandomized: unknown;
  Value: unknown;
}

/** unknown */
export interface HealthPotionAssignmentConditionSpec {
  MaxValue: unknown;
  MinValue: unknown;
}

/** request */
export interface HealthPotionConsumableTemplate {
  RestorePoints: number;
}

/** both */
export interface Hero {
  AttackRegions: AttackRegion;
  Equipment: unknown;
  EquippedConsumables: unknown;
  EquippedSpells: unknown;
  ExpirationDate: string;
  HeroSpecContainerId: number;
  HeroStatModifier: HeroStatModifier;
  Level: number;
  OwnerSpecialPacks: number;
  PriceReductionIds: number;
  Stats: unknown;
  XP: number;
}

/** request */
export interface HeroBiographyPanelNavigationModel {
  HeroTooltipModel: HeroTooltipModel;
  IsLocked: boolean;
  PanelName: number;
  SpecContainerId: number;
}

/** both */
export interface HeroConsumableCountChangedEventArgs {
  AbilitySlotIndex: number;
  SlotIndex: number;
  StackCount: number;
}

/** request */
export interface HeroConsumableEquipNotification {
  ConsumableItem: unknown;
  HeroSpecContainerId: number;
}

/** both */
export interface HeroConsumableEquippedEventArgs {
  ConsumableItem: unknown;
}

/** request */
export interface HeroConsumableItem {
  StackCount: number;
}

/** both */
export interface HeroConsumableSlot {
  SlotIndex: number;
  StackCount: number;
  TemplateId: number;
}

/** request */
export interface HeroConsumableUnequipNotification {
  HeroSpecContainerId: number;
  SlotIndex: number;
}

/** both */
export interface HeroConsumableUnequippedEventArgs {
  SlotIndex: number;
}

/** both */
export interface HeroCorpseHarvestHoverEventArgs {
  HeroCorpseHarvestHoverModel: HeroCorpseHarvestHoverModel;
}

/** request */
export interface HeroCorpseHarvestHoverModel {
  ElapsedTimeSinceDeath: number;
  FreeSlotsRequirement: number;
  HasItemsToCollect: boolean;
  HeroDisplayName: string;
  HeroIconModel: HeroIconModel;
  HeroLevel: number;
  HeroSpecContainerId: number;
  IsHeroInventoryLargeEnough: boolean;
  IsStorageFull: boolean;
}

/** unknown */
export interface HeroCorpseHarvestingSpec {
  PRO: unknown;
}

/** request */
export interface HeroCorpseHarvestingTooltipModel {
  CurrencyType: number;
  DeathTime: number;
  FreeSlotsRequirement: number;
  HasItemsToCollect: boolean;
  HeroDisplayName: string;
  HeroLevel: number;
  IconUrl: string;
  IsHeroInventoryLargeEnough: boolean;
  IsStorageFull: boolean;
  Type: number;
}

/** response */
export interface HeroCorpseSettings {
  HeroCorpseCooldownPerAttacker: string;
  HeroCorpseEffectIdsByHeroId: unknown;
  MaxHeroCorpsesInCastle: number;
}

/** both */
export interface HeroCreatedEventArgs {
  ErrorMessage: string;
  IsSuccess: boolean;
}

/** both */
export interface HeroCreationBiographyViewModel {
  HeroCreationHeroInfos: HeroCreationHeroInfo;
}

/** both */
export interface HeroCreationHeroInfo {
  CreationIconLeftOffset: number;
  CreationIconOverUrl: string;
  CreationIconSelectedUrl: string;
  CreationIconTopOffset: number;
  CreationIconUpUrl: string;
  IsLocked: boolean;
  SpecialPackGroup: number;
  TooltipModel: TooltipModel;
}

/** both */
export interface HeroDeathModel {
  CastleType: number;
  IsResurrectionAffordable: boolean;
  IsResurrectionAllowed: boolean;
  IsRevengeAttack: number;
  IsTestAttack: boolean;
  LoseTrophyCooldownRemainingTime: number;
  ResurrectionCost: number;
  TrophyScoreLost: number;
  TrophyScoreRestartAttackGain: number;
  TrophyScoreRestartAttackLost: number;
}

/** request */
export interface HeroDeathPanelNavigationModel {
  HeroDeathInfo: unknown;
}

/** request */
export interface HeroDyeAppliedNotification {
  DyeTemplateId: number;
  HeroItemSlot: number;
  HeroSpecContainerId: number;
}

/** request */
export interface HeroEquipConsumableCommand {
  EquippedSlotIndex: number;
  HeroId: number;
  TemplateId: number;
}

/** request */
export interface HeroEquipSpellCommand {
  HeroId: number;
  SlotIndex: number;
  SpellId: number;
}

/** request */
export interface HeroEquipment {
  Back: unknown;
  Body: unknown;
  Costume: unknown;
  Finger1: unknown;
  Hands: unknown;
  Head: unknown;
  MainHand: unknown;
  Neck: unknown;
  OffHand: unknown;
  Pet: unknown;
  Shoulders: unknown;
}

/** request */
export interface HeroEquipmentBuyBackSlot {
  Item: unknown;
}

/** unknown */
export interface HeroEquipmentDefinitionSpec {
  ArmorDamagePerLevel: unknown;
  AttackSpeedPerLevel: unknown;
  BaseArmorDamage: unknown;
  BaseAttackSpeed: unknown;
  BaseHealth: unknown;
  BaseRange: unknown;
  BaseResistance: unknown;
  BaseWeaponDamage: unknown;
  DefaultEquipmentTemplateIds: unknown;
  HealthPerLevel: unknown;
  HeroItemTypes: unknown;
  RangePerLevel: unknown;
  ResistancePerLevel: unknown;
  ShowcaseEquipmentTemplateIds: unknown;
  WeaponDamagePerLevel: unknown;
}

/** request */
export interface HeroEquipmentEquipCommand {
  DestinationSlot: number;
  HeroId: number;
  SourceSlotId: number;
}

/** request */
export interface HeroEquipmentEquipNotification {
  EquipmentItem: unknown;
  HeroItemSlot: number;
  HeroSpecContainerId: number;
}

/** both */
export interface HeroEquipmentEquippedEventArgs {
  EquippedHeroItem: unknown;
  WhenDyeApplied: boolean;
}

/** request */
export interface HeroEquipmentItem {
  ArchetypeId: number;
  DyeTemplateId: number;
  Effects: unknown;
  IsBranded: boolean;
  IsSellable: boolean;
  ItemLevel: number;
  PowerUp: unknown;
  PrimaryStatsModifiers: number;
  TemplateId: number;
}

/** both */
export interface HeroEquipmentRefreshedEventArgs {
  Equipment: unknown;
  HeroSpecContainerId: number;
}

/** request */
export interface HeroEquipmentUnequipCommand {
  DestinationSlotId: number;
  HeroId: number;
  SourceSlot: number;
}

/** request */
export interface HeroEquipmentUnequipNotification {
  HeroItemSlot: number;
  HeroSpecContainerId: number;
}

/** both */
export interface HeroEquipmentUnequippedEventArgs {
  ItemSlot: number;
  ItemType: unknown;
}

/** both */
export interface HeroEventArgs {
  CurrentHero: unknown;
  PreviousHero: unknown;
}

/** unknown */
export interface HeroFreeTrialCommunityEvent {
  HeroSpecContainerIds: unknown;
  IconUrl: unknown;
  PriceReductionConditionIds: unknown;
}

/** both */
export interface HeroFreeTrialInfoPeriod {
  Id: number;
  UnlockEndTime: string;
  UnlockStartTime: string;
}

/** request */
export interface HeroFreeTrialInfoViewedCommand {
  HeroFreeTrialInfoId: number;
}

/** both */
export interface HeroIconModel {
  HeroSpecContainerId: number;
  IconUrl: string;
  Level: number;
  SpecialPackGroup: number;
}

/** unknown */
export interface HeroInsideTriggerAssignmentConditionSpec {
  TriggerId: unknown;
}

/** request */
export interface HeroInventoryAddedNotification {
  InventorySlot: unknown;
  NewlyAdded: boolean;
}

/** both */
export interface HeroInventoryItemAddedEventArgs {
  GetHeroInventoryViewModel: GetHeroInventoryViewModel;
  HeroInventoryItem: unknown;
}

/** both */
export interface HeroInventoryItemModel {
  ConsumableType: number;
  DyeInfoModel: DyeInfoModel;
  EquippableItemSlots: unknown;
  HasRequiredLevel: boolean;
  HeroItemCategoryType: number;
  HeroItemType: HeroItemType;
  IconSynergyName: string;
  IconUrl: string;
  InventoryItemType: number;
  IsEquippable: boolean;
  IsLocked: boolean;
  IsMaxLevel: boolean;
  ItemDefinition: ItemDefinition;
  NewlyAdded: boolean;
  Quality: number;
  Rarity: number;
  SlotIndex: number;
  StackCount: number;
}

/** both */
export interface HeroInventoryItemRemovedEventArgs {
  GetHeroInventoryViewModel: GetHeroInventoryViewModel;
  InventoryItemType: number;
  SlotIndex: number;
}

/** both */
export interface HeroInventoryItemUpdatedEventArgs {
  GetHeroInventoryViewModel: GetHeroInventoryViewModel;
  InventoryItemType: number;
  NewlyAdded: boolean;
  SlotIndex: number;
  StackCount: number;
}

/** both */
export interface HeroInventoryNewItemCountChangedEventArgs {
  NewItemCount: number;
}

/** request */
export interface HeroInventoryPanelNavigationModel {
  GetEquippedItemsViewModel: GetEquippedItemsViewModel;
  GetHeroInventoryViewModel: GetHeroInventoryViewModel;
  GetHeroStatsModel: GetHeroStatsModel;
  PanelName: number;
}

/** both */
export interface HeroInventoryRefreshedEventArgs {
  GetHeroInventoryViewModel: GetHeroInventoryViewModel;
}

/** request */
export interface HeroInventoryRemovedNotification {
  SlotIndex: number;
}

/** both */
export interface HeroInventorySettings {
  DefaultIconLayerNames: unknown;
  EmptyIconLayerName: string;
  MissingIconLayerName: string;
  SlotBgLayerNames: unknown;
}

/** both */
export interface HeroInventorySlotUpdate {
  ItemType: number;
}

/** request */
export interface HeroInventorySlotUpdateForConsumable {
  ItemType: number;
}

/** request */
export interface HeroInventorySlotUpdateForHeroEquipment {
  HeroItem: HeroItem;
  ItemType: number;
}

/** request */
export interface HeroInventoryUpdatedNotification {
  SlotIndex: number;
  StackCount: number;
}

/** both */
export interface HeroItem {
  AcquisitionDate: string;
  SellPrice: number;
}

/** both */
export interface HeroItemArchetype {
  Damage: number;
  GearScoreMultiplier: number;
  HeroId: number;
  Range: number;
  Speed: number;
}

/** unknown */
export interface HeroItemArchetypesSettings {
  ArmorArchetypes: unknown;
  PrimaryStatCount: unknown;
  WeaponArchetypes: unknown;
}

/** both */
export interface HeroItemBuildingRequirement {
  BuildingRequirementRank: number;
  BuildingRequirementSpecContainerId: number;
  MaxLevel: number;
  MinLevel: number;
}

/** unknown */
export interface HeroItemBuildingRequirementSettings {
  Requirements: unknown;
}

/** unknown */
export interface HeroItemCategories {
  CategoryList: unknown;
}

/** both */
export interface HeroItemCategory {
  AllowedEffects: unknown;
  CategoryType: number;
  IsItemLevelHidden: boolean;
}

/** request */
export interface HeroItemEffectTemplate {
  BaseValue: number;
  DebugName: string;
  EffectCategory: number;
  FormatValueAsPercentage: boolean;
  FormatValuePrecision: number;
  FormatWithPlusSign: boolean;
  Id: number;
  LayerName: string;
  LevelReplacementIcon: string;
  LevelReplacementThreshold: number;
  MaxItemLevel: number;
  MinItemQuality: number;
  NamedItemEffectLevelUnlock: NamedItemEffectLevelUnlock;
  OasisDescription: number;
  OasisName: number;
  RandomChance: number;
  Type: number;
  ValuePerLevel: number;
}

/** unknown */
export interface HeroItemLootSelectionSpec {
  HeroItemQualityMask: unknown;
}

/** both */
export interface HeroItemPrimaryStats {
  HeroItemArchetype: HeroItemArchetype;
  StatMaxValues: number;
  StatValues: number;
}

/** both */
export interface HeroItemQualityFxCollection {
  Fx: unknown;
}

/** unknown */
export interface HeroItemSellSettings {
  SellBasePrices: unknown;
  SellQualityModifiers: unknown;
  SellRarityModifiers: unknown;
}

/** unknown */
export interface HeroItemSpecContainer {
  Type: unknown;
}

/** unknown */
export interface HeroItemSpecContainerRef {
  SpecContainerReferenceId: unknown;
}

/** unknown */
export interface HeroItemTemplate {
  AbilityId: unknown;
  ArchetypeId: unknown;
  AttackImpactSoundId: unknown;
  DefaultDyeTemplateIds: unknown;
  DescriptionId: unknown;
  HeroItemTypeId: unknown;
  Id: unknown;
  InternalDescription: unknown;
  InventoryMaxStackCount: unknown;
  InvIconUrl: unknown;
  IsDyeable: unknown;
  IsRare: unknown;
  IsUpgradable: unknown;
  LevelMax: unknown;
  LevelMin: unknown;
  MeshModel: unknown;
  MeshModels: unknown;
  OasisID: unknown;
  Rarity: unknown;
  ShopIconUrl: unknown;
  SoundArmorTag: unknown;
  SteamAssetSpec: unknown;
  SteamAssetUiSpec: unknown;
  Effects: unknown;
  IsDroppable: unknown;
  PowerUp: unknown;
  SuperVFX: unknown;
  VFX: unknown;
}

/** unknown */
export interface HeroItemTemplates {
  TemplateList: unknown;
}

/** response */
export interface HeroItemTextParams {
  BackgroundColor: number;
  BackgroundMarginX: number;
  BackgroundMarginY: number;
  Colors: unknown;
  FontParams: number;
  HeightOffset: number;
}

/** response */
export interface HeroItemType {
  EquipUserInterfaceSoundId: number;
  HeroItemCategoryType: number;
  Id: number;
  InternalDescription: string;
  OasisID: number;
  VisualType: number;
}

/** both */
export interface HeroItemTypeElement {
  HeroItemTypeId: number;
  RandomChance: number;
}

/** unknown */
export interface HeroItemTypes {
  ItemTypeList: unknown;
}

/** unknown */
export interface HeroLevelAssignmentConditionSpec {
  MaxLevel: unknown;
  MinLevel: unknown;
}

/** request */
export interface HeroLevelReachedObjectiveRequirement {
  Level: number;
}

/** unknown */
export interface HeroLevelUpAssignmentTriggerSpec {
  Level: unknown;
}

/** request */
export interface HeroLevelUpFriendNewsData {
  HeroLevel: number;
  HeroName: string;
  HeroSpecContainerId: number;
}

/** request */
export interface HeroLevelUpOwnNewsData {
  HeroLevel: number;
  HeroName: string;
  HeroSpecContainerId: number;
}

/** request */
export interface HeroLevelUpPanelNavigationModel {
  ExcludeModalPopupOpening: boolean;
  HeroUpgradeModel: HeroUpgradeModel;
  IsOpalPanel: boolean;
  PanelName: number;
}

/** request */
export interface HeroLevelUpReadyPanelNavigationModel {
  HeroSpecContainerId: number;
  Level: number;
}

/** both */
export interface HeroModel {
  Biography: string;
  CanAfford: boolean;
  Description: string;
  HeroFullName: string;
  IconUrl: string;
  IsHeroOwned: boolean;
  IsInFreeTrial: boolean;
  IsSpecialPack: boolean;
  LongHeroName: string;
  PriceReductionConditionModels: PriceReductionConditionModel;
  RegularPrice: unknown;
  SpecContainerId: number;
}

/** both */
export interface HeroModifier {
  HeroCreationIconLeftOffset: number;
  HeroCreationIconOverUrl: string;
  HeroCreationIconSelectedUrl: string;
  HeroCreationIconTopOffset: number;
  HeroCreationIconUpUrl: string;
  HeroIconUrl: string;
  HeroPortraitUrl: string;
  HeroRoundedIconUrl: string;
  HeroRoundedLargeIconUrl: string;
  HeroShopIconUrl: string;
  HeroVisualGroupNames: unknown;
  StatModifierIconUrl: string;
  StatModifierOasisDescription: number;
  Stats: unknown;
  TooltipIconUrl: string;
}

/** unknown */
export interface HeroNamedItem {
  Effects: unknown;
  IsDroppable: unknown;
  PowerUp: unknown;
  SuperVFX: unknown;
  VFX: unknown;
}

/** both */
export interface HeroProfileViewModel {
  Equipment: unknown;
  EquippedSpells: unknown;
  GetHeroStatsModel: GetHeroStatsModel;
}

/** both */
export interface HeroSampleSkillModel {
  IconUrl: string;
  LayerName: string;
  Name: string;
  SpecContainerId: number;
}

/** request */
export interface HeroSelectedNotification {
  HeroSpecContainerId: number;
}

/** both */
export interface HeroSelectionModel {
  Description: string;
  HeroSpecContainerId: number;
  IconUrl: string;
  IsCurrentHero: boolean;
  IsOwned: boolean;
  IsSpecialPack: boolean;
  Level: number;
  Name: string;
  Requirement: string;
  SkuCode: string;
  SpecialPackGroup: number;
}

/** request */
export interface HeroSelectionPanelNavigationModel {
  CurrentHeroSpecContainerId: number;
  HeroSelections: unknown;
  LayerName: string;
}

/** unknown */
export interface HeroSettings {
  CriticalHitBonusLevelRange: unknown;
  DodgeBonusLevelRange: unknown;
  DPSPerPower: unknown;
  FragmentsPerHealthOrb: unknown;
  GlobalHeroDamageMultiplier: unknown;
  GlobalHeroHealthMultiplier: unknown;
  HealthPerVitality: unknown;
  HeroDamageDealtMultipliers: unknown;
  HeroDamageReceivedMultipliers: unknown;
  HeroStunResistanceLossPerSecond: unknown;
  HeroStunResistanceMultiplier: unknown;
  LevelRequirements: unknown;
  ManaPerEnergy: unknown;
  MaxCriticalHitChance: unknown;
  MaxDodgeChance: unknown;
  MaxEquippedConsumables: unknown;
  MaxEquippedSpells: unknown;
  MinCriticalHitChance: unknown;
  MinDodgeChance: unknown;
  PerLevelRangeCriticalHitBonus: unknown;
  PerLevelRangeDodgeBonus: unknown;
  PetSpawnableEntitySpecs: unknown;
  UnlockedHeroesSpecIds: unknown;
  XpPerLevel: unknown;
}

/** unknown */
export interface HeroSpec {
  HighPickingHeight: unknown;
  UseHighPickingStyle: unknown;
}

/** unknown */
export interface HeroSpecContainer {
  Type: unknown;
  SpecContainerReferenceId: unknown;
}

/** unknown */
export interface HeroSpecContainerRef {
  SpecContainerReferenceId: unknown;
}

/** both */
export interface HeroSpellNewItemCountChangedEventArgs {
  NewItemCount: number;
}

/** both */
export interface HeroSpellSlot {
  SlotIndex: number;
  SpellSpecContainerId: number;
}

/** unknown */
export interface HeroSpellsSpec {
  AllowedSpells: unknown;
}

/** both */
export interface HeroStat {
  StatType: number;
}

/** both */
export interface HeroStatModifier {
  StatType: number;
  Value: number;
}

/** both */
export interface HeroStatsModel {
  EquipmentAbilities: unknown;
  MaxResistance: number;
  Stats: unknown;
  WeightType: number;
}

/** unknown */
export interface HeroStatsSpec {
  BaseControlResistance: unknown;
  BaseCriticalDamage: unknown;
  BaseCriticalHitChance: unknown;
  BaseDamage: unknown;
  BaseDodgeChance: unknown;
  BaseGrip: unknown;
  BaseHealth: unknown;
  BaseHealthRegeneration: unknown;
  BaseMana: unknown;
  BaseManaRegeneration: unknown;
  BaseMovementSpeed: unknown;
  ControlResistancePerLevel: unknown;
  DamagePerLevel: unknown;
  FastManaFlow: unknown;
  FastMoveSpeed: unknown;
  GripPerLevel: unknown;
  HealthPerLevel: unknown;
  HealthRegenerationPerLevel: unknown;
  ManaPerLevel: unknown;
  ManaRegenerationPerLevel: unknown;
  NormalManaFlow: unknown;
  NormalMoveSpeed: unknown;
  SlowManaFlow: unknown;
  SlowMoveSpeed: unknown;
}

/** both */
export interface HeroStatsSummaryChangedEventArgs {
  HeroStatsSummaryModel: HeroStatsSummaryModel;
}

/** both */
export interface HeroStatsSummaryModel {
  HeroLevel: number;
  HeroName: string;
  HeroPictureUrl: string;
  LevelExperienceStats: unknown;
}

/** request */
export interface HeroTooltipModel {
  Biography: string;
  Level: number;
  LongHeroName: string;
  SampleSkills: unknown;
  SpecContainerId: number;
  SpecialPackGroup: number;
  StatModifierDescription: string;
  StatModifierIconUrl: string;
  TooltipIconUrl: string;
  Type: number;
}

/** request */
export interface HeroTrainerBuildingInfoDataModel {
  CurrentMaxHeroLevel: number;
  MaxMaxHeroLevel: number;
}

/** request */
export interface HeroTrainerBuildingUpgradePopupModel {
  NewMaxHeroLevel: number;
}

/** unknown */
export interface HeroUiSpec {
  BiographyNoNameOasisId: unknown;
  BiographyOasisId: unknown;
  CreationIconLeftOffset: unknown;
  CreationIconOverUrl: unknown;
  CreationIconSelectedUrl: unknown;
  CreationIconTopOffset: unknown;
  CreationIconUpUrl: unknown;
  DescriptionOasisId: unknown;
  FullNameOasisId: unknown;
  HeaderIconUrl: unknown;
  HeroIconLrgBgLayerName: unknown;
  IconLayerName: unknown;
  IconUrl: unknown;
  NameOasisId: unknown;
  PortraitUrl: unknown;
  RoundedIconUrl: unknown;
  RoundedLargeIconUrl: unknown;
  SampleAbilities: unknown;
}

/** both */
export interface HeroUnequipSpellCommand {
  HeroId: number;
  SlotIndex: number;
}

/** request */
export interface HeroUnlockRewardItem {
  ExpirationDate: string;
  HeroSpecContainerId: number;
}

/** request */
export interface HeroUnlockedNotification {
  Hero: Hero;
}

/** both */
export interface HeroUpgradeModel {
  BuildingRequirementName: string;
  BuildingRequirementRank: number;
  CanAfford: boolean;
  CurrentDPS: number;
  CurrentHealth: number;
  CurrentLevelXp: number;
  CurrentMagicalArmor: number;
  CurrentMana: number;
  CurrentPhysicalArmor: number;
  CurrentXp: number;
  DPSIncrease: number;
  HealthIncrease: number;
  HeroIconModel: HeroIconModel;
  IsBuildingRequirementMet: boolean;
  IsXpRequirementMet: boolean;
  LongHeroName: string;
  MagicalArmorIncrease: number;
  ManaIncrease: number;
  MaxDPS: number;
  MaxHealth: number;
  MaxMagicalArmor: number;
  MaxMana: number;
  MaxPhysicalArmor: number;
  NextLevel: number;
  PhysicalArmorIncrease: number;
  SpecContainerId: number;
  UnlockedAbilities: unknown;
  XpRequirement: number;
}

/** request */
export interface HeroUpgradePanelNavigationModel {
  HeroModel: HeroModel;
  PanelName: number;
}

/** request */
export interface HeroUpgradeTooltipModel {
  DPSIncrease: number;
  HealthIncrease: number;
  IsXpRequirementMet: boolean;
  LongHeroName: string;
  ManaIncrease: number;
  NextLevel: number;
  SpecContainerId: number;
  Type: number;
  UnlockedAbilities: unknown;
  XpRequirement: number;
}

/** both */
export interface HeroUpgradeUnlockedAbilityModel {
  AbilityLevel: number;
  IconUrl: string;
  Name: string;
  SpecContainerId: number;
}

/** unknown */
export interface HeroVoicesSounds {
  AllMinesDestroyedVo: unknown;
  AllStorageChestsOpenedVo: unknown;
  AttackTimerReachedZeroVo: unknown;
  BossAggroedVo: unknown;
  BossKilledVo: unknown;
  BuildingUpgradedVo: unknown;
  CannotUseSkillWhileStunnedVo: unknown;
  CastleEntranceVo: unknown;
  CreatureUpgradedVo: unknown;
  DecorationDestroyedVo: unknown;
  DrinkPotionVo: unknown;
  EquipsGearVo: unknown;
  InflictsCriticalDamageVo: unknown;
  InventoryIsFullVo: unknown;
  KilledVo: unknown;
  KillingCreaturesOverTimeVoConfig: unknown;
  LevelUpVo: unknown;
  LowHealthVo: unknown;
  MaxDefensePointReachedVo: unknown;
  MaxXpReachedVo: unknown;
  PickUpLifeOrbVo: unknown;
  PlacingBossCreatureVo: unknown;
  PlacingRoomVo: unknown;
  PurchasingGearVo: unknown;
  PurhasingPotionVo: unknown;
  ReceiveCriticalDamageVoConfig: unknown;
  ResurrectedVo: unknown;
  SellingGearVo: unknown;
  StorageChestsAreShieldedVo: unknown;
  TreasureRoomDoorOpeningVo: unknown;
  Description: unknown;
}

/** request */
export interface HeroXpChangedNotification {
  HeroSpecContainerId: number;
  Level: number;
  LevelChanged: boolean;
  TotalXp: number;
  XpAdded: number;
}

/** both */
export interface HeroesEventArgs {
  Heroes: unknown;
}

/** unknown */
export interface HideAttackSelectionCastlesAssignmentActionSpec {
  CastleIds: unknown;
}

/** unknown */
export interface HideShopItemsOnlyAssignmentActionSpec {
  IsDisabled: unknown;
  ShopItems: unknown;
}

/** both */
export interface HideTooltipEventArgs {
  Id: number;
}

/** unknown */
export interface HideableSpec {
  IsVisible: unknown;
}

/** both */
export interface HitInformation {
  DamageSource: number;
  DamageValue: number;
  DefenseIngredientId: number;
  Details: unknown;
  HitSuccess: number;
  HitTotal: number;
  SpecContainerId: number;
}

/** both */
export interface HitInformationDetail {
  DamageValue: number;
  HeroGlobalX: number;
  HeroGlobalZ: number;
  HeroX: number;
  HeroY: number;
}

/** both */
export interface HomePanelButtonSettings {
  ButtonContainer: string;
  Index: number;
  NavigationURL: string;
  OasisID: number;
}

/** both */
export interface HudAbilityCancelledEventArgs {
  AbilitySlotIndex: number;
}

/** both */
export interface HudAbilityCooldownEndedEventArgs {
  AbilitySlotIndex: number;
}

/** both */
export interface HudAbilityCooldownModel {
  AbilitySlotIndex: number;
  ChargeUpRatio: number;
  CooldownRatio: number;
  InvalidAttackActionType: number;
  PowerUpRatio: number;
}

/** both */
export interface HudAbilityCooldownUpdatedEventArgs {
  HudAbilityCooldownModels: HudAbilityCooldownModel;
}

/** both */
export interface HudAbilityLaunchedEventArgs {
  AbilitySlotIndex: number;
  CooldownDuration: number;
}

/** both */
export interface HudCastleValidationKillCountUpdatedEventArgs {
  KilledCreaturesCount: number;
  TotalCreaturesCount: number;
}

/** both */
export interface HudCastleValidationMineCountUpdatedEventArgs {
  DestroyedMineCount: number;
  TotalMineCount: number;
}

/** both */
export interface HudCastleValidationTimeUpdatedEventArgs {
  Time: number;
}

/** both */
export interface HudEnemyTargettedEventArgs {
  BossPictureVariable: string;
  BuffsViewModel: unknown;
  GameEntityId: number;
  GameEntityType: number;
  HideLevelInHud: boolean;
  Level: number;
  Life: number;
  MaxLife: number;
  Name: string;
  Rank: number;
  Tier: number;
}

/** both */
export interface HudHeroInfoModel {
  CurrentLevelXp: number;
  IconLayerName: string;
  IsMaxLevel: number;
  Level: number;
  Life: number;
  Mana: number;
  MaxLife: number;
  MaxMana: number;
  NextLevelXp: number;
  PortraitUrl: string;
  Xp: number;
}

/** both */
export interface HudHeroLevelUpEventArgs {
  HeroSpecContainerId: number;
  NewLevel: number;
}

/** request */
export interface HudItemLootedEventArgs {
  DyeInfoModel: DyeInfoModel;
  IconTexture: string;
  IGC: number;
  ItemName: string;
  ItemQuality: number;
  LifeForce: number;
  LootType: number;
}

/** both */
export interface HudLifeChangedEventArgs {
  DelayedLife: number;
  Life: number;
  MaxLife: number;
}

/** both */
export interface HudManaChangedEventArgs {
  FromRegen: boolean;
  Mana: number;
  MaxMana: number;
  PreviousMana: number;
}

/** request */
export interface HudPanelNavigationModel {
  CurrentArmor: number;
  CurrentHealth: number;
  CurrentLevelXp: number;
  CurrentMana: number;
  CurrentResistance: number;
  EquippedConsumablesViewModel: unknown;
  EquippedSpellViewModel: unknown;
  HudType: number;
  IGC: number;
  IsInAttack: boolean;
  IsTestAttack: boolean;
  LifeForce: number;
  MaxArmor: number;
  MaxHealth: number;
  MaxIGC: number;
  MaxLifeForce: number;
  MaxMana: number;
  MaxResistance: number;
  NewCountByIcons: unknown;
  NewObjectives: number;
  NextLevelXp: number;
  PremiumCash: number;
  XP: number;
}

/** both */
export interface HudResistanceChangedEventArgs {
  MaxResistance: number;
  Resistance: number;
}

/** both */
export interface HudReturnToLobbyEventArgs {
  CanPayToKeepItems: boolean;
  LootTransferenceCost: number;
}

/** both */
export interface HudXpChangedEventArgs {
  CurrentLevelXp: number;
  IsMaxLevel: boolean;
  Level: number;
  NextLevelXp: number;
  Xp: number;
}

/** unknown */
export interface IfNotNullOperationSpec {
  Operations: unknown;
  Value: unknown;
}

/** unknown */
export interface ImmunityBuffEffectSpec {
  ImmunityTypeMask: unknown;
}

/** unknown */
export interface ImmunitySpec {
  ImmuneToDamageFrom: unknown;
  ImmunityTypeMask: unknown;
}

/** request */
export interface InboxCollectCommand {
  SlotIndexes: unknown;
}

/** request */
export interface InboxCollectToBuyBackCommand {
  BuybackId: string;
  ObjectId: string;
}

/** request */
export interface InboxCollectToHeroEquipmentCommand {
  HeroId: number;
  HeroItemSlot: number;
}

/** request */
export interface InboxCollectToHeroInventoryCommand {
  SlotIndexes: unknown;
}

/** request */
export interface InboxConsumableItem {
  HeroItem: HeroItem;
  ItemType: number;
}

/** request */
export interface InboxHeroEquipmentItem {
  HeroItem: HeroItem;
  ItemType: number;
  ItemType: number;
  ObjectId: string;
}

/** both */
export interface InboxItem {
  HeroItem: HeroItem;
  ItemType: number;
  ItemType: number;
  ObjectId: string;
}

/** request */
export interface InboxItemsAddedNotification {
  InboxItems: InboxItem;
}

/** unknown */
export interface IncrementSavedValueOperationSpec {
  Increment: unknown;
}

/** request */
export interface InstallCompletedTaskTracking {
  Duration: number;
  IsFirstInstall: boolean;
}

/** request */
export interface InstallPackageCompletedTracking {
  Duration: number;
  IsSuccessful: boolean;
  PackageVersionId: unknown;
}

/** request */
export interface InstallPackageStartedTracking {
  PackageVersionId: unknown;
  PatchFlags: number;
  VersionName: string;
}

/** request */
export interface InstallStartedTaskTracking {
  IsFirstInstall: boolean;
  CreationDate: string;
  TrackingTagId: number;
}

/** unknown */
export interface InteractionStartedAssignmentTriggerSpec {
  EffectSpecContainerId: unknown;
}

/** unknown */
export interface InteractiveSpec {
  ChangeInteractorOrientation: unknown;
  DeactivateAfterFirstInteraction: unknown;
  Distance: unknown;
  InteractionActivationTrigger: unknown;
  InteractionPointOffset: unknown;
  InteractiveDuration: unknown;
  InteractorDuration: unknown;
  InteractorOrientation: unknown;
  IsInteractorInvincibleDuringInteraction: unknown;
  MustBeAsCloseAsPossible: unknown;
  Operations: unknown;
  ResetToPreviousInvincibilityStateAfterInteraction: unknown;
  StartInteractiveDelay: unknown;
  StartOperations: unknown;
}

/** both */
export interface InternalTooltipOptions {
  callback: string;
  fadeIn: number;
  fadeOut: number;
  JQueryTemplate: string;
  left: number;
  top: number;
}

/** request */
export interface InvalidActionFeedback {
  Priority: number;
}

/** request */
export interface InvalidAttackActionsFeedbacks {
  CannotCollectLoot_InventoryIsFull: unknown;
  CannotDrinkPotion_FullHealth: unknown;
  CannotDrinkPotion_OutOfPotion: unknown;
  CannotUseSkill_BusyWithAnotherAction: unknown;
  CannotUseSkill_Cooldown: unknown;
  CannotUseSkill_Disabled: unknown;
  CannotUseSkill_OutOfMana: unknown;
  CannotUseSkill_Silenced: unknown;
  CannotUseSkill_Stunned: unknown;
}

/** unknown */
export interface InvalidBuildActionAssignmentTriggerSpec {
  GameEntityTypeMask: unknown;
  ResultFlags: unknown;
}

/** request */
export interface InvalidBuildActionsFeedbacks {
  BossNotInBossRoom: unknown;
  CannotAddSecondBoss: unknown;
  CannotCloneStampEntity: unknown;
  CannotDropInEntranceRoom: unknown;
  CannotPlaceMoreDecorationsInRoom: unknown;
  CannotPlaceMoreRooms: unknown;
  CannotPlaceSecondEntranceRoom: unknown;
  CannotPlaceSecondThroneRoom: unknown;
  CannotPlaceTotemInBossRoom: unknown;
  CannotRemoveEntranceRoom: unknown;
  CannotRemoveThroneRoom: unknown;
  CpZoneHasNotEnoughCapacity: unknown;
  CreaturePivotNotInCapacityBoosterZone: unknown;
  EntitySectionsOverlapping: unknown;
  ExceedingCastleMaxCp: unknown;
  InvalidBoostTarget: unknown;
  NoOtherPossibleOrientations: unknown;
  RoomBuildableOverInvalidGround: unknown;
  RoomBuildableOverRoomJunction: unknown;
  RoomOutOfCastleGrid: unknown;
  TrapExclusionRadiusColliding: unknown;
}

/** request */
export interface InvalidCastleFeedbacksInfos {
  FeedbackTitleText: unknown;
  NoCreatures: unknown;
  NoEntranceRoom: unknown;
  NoPathToThroneRoom: unknown;
  NotEnoughRooms: unknown;
  NoThroneRoom: unknown;
  UnconnectedRooms: unknown;
}

/** request */
export interface InventoryBuyTabPanelNavigationModel {
  CanAfford: boolean;
  Price: unknown;
  SkuCode: string;
}

/** both */
export interface InventoryConsumablesInfo {
  StackCount: number;
  TemplateId: number;
}

/** request */
export interface InventoryDecoration {
  Level: number;
}

/** request */
export interface InventoryDefenseIngredientBoost {
  Level: number;
}

/** both */
export interface InventoryItem {
  ArchetypeId: number;
  DyeTemplateId: number;
  Effects: unknown;
  IsBranded: boolean;
  IsSellable: boolean;
  ItemLevel: number;
  PowerUp: unknown;
  PrimaryStatsModifiers: number;
  TemplateId: number;
}

/** unknown */
export interface InventoryItemAddedAssignmentTriggerSpec {
  UsedInventorySlotsCount: unknown;
}

/** unknown */
export interface InventoryItemOwnedAssignmentConditionSpec {
  InventoryItemType: unknown;
  TemplateIds: unknown;
}

/** request */
export interface InventoryItemRewardItem {
  Item: unknown;
}

/** both */
export interface InventoryItemWithGenerationInfo {
  InventoryItem: InventoryItem;
  ItemGenerationInfo: ItemGenerationInfo;
}

/** request */
export interface InventoryMoveItemCommand {
  Count: number;
  DestinationInventory: number;
  DestinationSlotId: number;
  SourceInventory: number;
  SourceSlotId: number;
}

/** request */
export interface InventoryPanelNavigationModel {
  IsInventoryOpenedChangingTab: boolean;
}

/** request */
export interface InventoryRoom {
  Level: number;
}

/** unknown */
export interface InventorySettings {
  BuyBackTimeoutForInventoryFull: unknown;
  InventorySlotByTabCount: unknown;
  InventoryTabMaxCount: unknown;
}

/** request */
export interface InventorySwapItemCommand {
  DestinationSlotId: number;
  SourceSlotId: number;
}

/** both */
export interface InventoryTabAddedEventArgs {
  GetHeroInventoryViewModel: GetHeroInventoryViewModel;
}

/** request */
export interface InventoryTabAddedNotification {
  InventoryTabCount: number;
}

/** both */
export interface InventoryTabModel {
  AvailableSlots: number;
  IconUrl: string;
  Name: string;
  TabIndex: number;
  TabSize: number;
}

/** request */
export interface InventoryTabRewardItem {
  Count: number;
}

/** both */
export interface InventoryTemplate {
  Creatures: unknown;
  Decorations: unknown;
  DefenseIngredientBoosts: unknown;
  Heroes: unknown;
  HeroItems: HeroItem;
  InventoryTabCount: number;
  Rooms: unknown;
  Traps: unknown;
  UnlockedEmotes: number;
}

/** unknown */
export interface IsEntityHasBuffOperationSpec {
  BuffSpecContainersIds: unknown;
}

/** unknown */
export interface IsEntityOneOfOperationSpec {
  SpecContainersIds: unknown;
}

/** unknown */
export interface ItemAbilitySettings {
  ItemAbilities: unknown;
  StatTypesItemAbilities: unknown;
}

/** unknown */
export interface ItemAbilitySpec {
  DebugName: unknown;
  IsPercentage: unknown;
  IsSpellTrigger: unknown;
  TooltipDescriptionOasisId: unknown;
  TooltipNoAbilityOasisId: unknown;
  UseAbsoluteValue: unknown;
}

/** unknown */
export interface ItemAbilityValueSpec {
  Base: unknown;
  ItemAbilityId: unknown;
  Multiplier: unknown;
}

/** both */
export interface ItemDefinition {
  HasRequiredLevel: boolean;
  IsEquipable: boolean;
  ItemHtmlTag: string;
  ItemId: number;
  ItemType: number;
}

/** both */
export interface ItemEffect {
  Id: number;
  Level: number;
  Type: number;
}

/** both */
export interface ItemGenerationInfo {
  GenerationNumber: number;
  GenerationSystem: number;
}

/** unknown */
export interface ItemOwningCountObjective {
  Count: unknown;
  ItemType: unknown;
  TemplateId: unknown;
}

/** both */
export interface ItemPowerUp {
  Id: number;
  Level: number;
}

/** unknown */
export interface ItemPurchasedAssignmentTriggerSpec {
  ItemId: unknown;
  ItemType: unknown;
}

/** both */
export interface ItemPurchasedEventArgs {
  ShopSku: ShopSku;
}

/** both */
export interface JobStrategy {
  JobType: number;
  RetryCount: number;
  RetryInterval: number;
}

/** both */
export interface JobSummary {
  DueDate: string;
  Id: string;
  ProcessingServer: string;
  RetryCount: number;
  Status: number;
  Type: number;
}

/** both */
export interface JoinRequestModel {
  AcceptInhibitedAsGuildFull: boolean;
  AccountSummary: AccountSummary;
  AvatarLayerName: string;
}

/** request */
export interface KillEntitiesAchievement {
  BossCreaturesOnly: boolean;
  CreatureIds: number;
  EntityType: number;
}

/** unknown */
export interface KillEntitiesObjective {
  CreatureIds: unknown;
  EntityType: unknown;
}

/** both */
export interface KillingCreaturesOverTimeVoConfig {
  CreaturesCount: number;
  TimePeriod: number;
  Vo: unknown;
}

/** unknown */
export interface KnockbackSpec {
  CheckStunImmunity: unknown;
  KnockbackOnGroundDuration: unknown;
  KnockbackStandupDuration: unknown;
  KnockbackStyle: unknown;
  UseTrapStunDurationReductionStat: unknown;
}

/** unknown */
export interface LabelOperationListenerConditionSpec {
  OperationLabel: unknown;
}

/** response */
export interface LanguageTranslation {
  Language: string;
  Translations: unknown;
}

/** both */
export interface LastVisitedShop {
  Url: string;
}

/** unknown */
export interface LaunchAttackAssignmentActionSpec {
  GameStateModifier: unknown;
  UbisoftCastleId: unknown;
}

/** both */
export interface LaunchAttackParam {
  AccountId: number;
  CastleType: number;
  PosX: number;
  PosY: number;
}

/** both */
export interface LeaderLeaderboardEntryModel {
  LeaderEntryModel: unknown;
  RewardModel: RewardModel;
}

/** both */
export interface LeaderboardEntry {
  AccountSummary: AccountSummary;
  IsCastleAttackable: boolean;
  Score: number;
  Seconds: number;
}

/** both */
export interface LeaderboardEntryModel {
  AccountSummary: AccountSummary;
  AvatarUrl: string;
  Country: Country;
  IsCastleAttackable: boolean;
  IsCastleAttackableForTargetedAttack: boolean;
  IsDemoted: boolean;
  IsPromoted: boolean;
  NextSeasonSubLeagueModel: unknown;
  Rank: number;
  Score: number;
  SpecialPackModel: SpecialPackModel;
  SubLeagueModel: SubLeagueModel;
}

/** both */
export interface LeaderboardFiltersModel {
  Filters: Filter;
  LeagueFilterModels: LeagueFilterModel;
  SelectedFilterCode: string;
  SelectedLeagueId: number;
  SelectedSubLeagueId: number;
}

/** both */
export interface LeaderboardPage {
  ActiveCountries: unknown;
  ActiveZones: unknown;
  CurrentUser: unknown;
  Entries: unknown;
  FirstEntryRank: number;
  Leaders: unknown;
  NextSeasonStartingDate: string;
  PreviousLeagueInfo: PreviousLeagueInfo;
  RemainingTime: number;
  SeasonalReward: unknown;
  TotalCount: number;
  WorldLeader: unknown;
}

/** both */
export interface LeaderboardProgressBarModel {
  NextSubLeagueDetailedModel: unknown;
  PreviousSubLeagueDetailedModel: unknown;
}

/** unknown */
export interface LeaderboardSettings {
  CacheValidity: unknown;
  RedisAccessabilityVerificationTime: unknown;
}

/** both */
export interface League {
  Id: number;
  LargeIconUrl: string;
  Name: unknown;
  SmallIconUrl: string;
  SubLeagues: SubLeague;
}

/** both */
export interface LeagueFilterModel {
  LeagueId: number;
  Name: string;
  SubLeagueId: number;
}

/** both */
export interface LeagueModel {
  LargeIconUrl: string;
  Name: string;
  ScoreMax: number;
  ScoreMin: number;
  SmallIconUrl: string;
  SubLeagueModels: SubLeagueModel;
}

/** request */
export interface LeaguePopupModel {
  CurrentSubLeagueModel: unknown;
  CurrentSubLeagueReward: unknown;
  IsDemoted: boolean;
  IsLeagueRanked: boolean;
  IsMaintained: boolean;
  IsPlaced: boolean;
  IsPromoted: boolean;
  IsUnranked: boolean;
  IsWorldRanked: boolean;
  NextSeasonStartingDate: string;
  PreviousLeagueRank: number;
  PreviousSubLeagueReward: unknown;
  PreviousWorldRank: number;
  SeasonalReward: unknown;
  SeasonalRewardTooltip: unknown;
}

/** request */
export interface LeaguePopupPanelNavigationModel {
  IsOpalPanel: boolean;
  LeaguePopupModel: LeaguePopupModel;
  PanelName: number;
}

/** request */
export interface LeagueProgressionPanelNavigationModel {
  CurrentLeagueId: number;
  CurrentSubLeagueId: number;
  IsLastLeagueSelected: boolean;
  LeagueModels: LeagueModel;
  SelectedLeagueId: number;
  SelectedSubLeagueId: number;
  SubLeagueDetailedModel: SubLeagueDetailedModel;
}

/** request */
export interface LeagueRankReachedNewsData {
  IsMaintained: boolean;
  IsPromoted: boolean;
  LeagueId: number;
  LeagueRank: number;
  SubLeagueId: number;
  SubLeagueName: string;
  SubLeaguePrefixName: string;
  SubLeagueSmallIconUrl: string;
}

/** request */
export interface LeagueUpdatedNewsData {
  CurrentLeagueId: number;
  CurrentSubleagueId: number;
  IsDemoted: boolean;
  IsMaintained: boolean;
  IsPlaced: boolean;
  IsPromoted: boolean;
  IsUnranked: boolean;
  PreviousLeagueId: number;
  PreviousSubleagueId: number;
  SubLeagueName: string;
  SubLeaguePrefixName: string;
  SubLeagueSmallIconUrl: string;
}

/** request */
export interface LeagueUpdatedNotification {
  LeagueId: number;
  SubLeagueId: number;
}

/** request */
export interface LeaveCastlePanelNavigationModel {
  CastleType: number;
  DefenderCastleName: string;
  HeroSpecContainerId: number;
  IsCastleValidated: boolean;
  IsPvECompetition: boolean;
  IsTestAttack: boolean;
  IsThemePreview: boolean;
  TrophyScoreLost: number;
}

/** both */
export interface LegalNotice {
  Copyrights: unknown;
  SpecializationName: string;
  SpecializationNameOasisId: number;
}

/** both */
export interface LevelDifferenceModifier {
  Lose: number;
  Win: number;
}

/** both */
export interface LevelExperienceStatsModel {
  currentXp: number;
  nextLevelXp: number;
  previousLevelXp: number;
}

/** both */
export interface LevelProductionPack {
  Level: number;
  RandomQualityQuantity: number;
}

/** both */
export interface LevelRenovationCompletionInformation {
  DescriptionOasisId: number;
  LayerName: string;
  TitleOasisId: number;
}

/** both */
export interface LevelRenovationInformation {
  Cost: unknown;
  LevelNameOasisId: number;
  LevelRenovationCompletionInformation: LevelRenovationCompletionInformation;
  RewardNameOasisId: number;
}

/** unknown */
export interface LevelUpPriceReductionCondition {
  Level: unknown;
}

/** both */
export interface LevelsDifferenceXpModifier {
  LevelsDifference: number;
  XpModifier: number;
}

/** request */
export interface LifeForceBoostConsumableTemplate {
  AttackIncreasedLifeForce: number;
  MineIncreasedLifeForce: number;
}

/** unknown */
export interface LifeSelectionSpec {
  MaxLifePercentage: unknown;
  MinLifePercentage: unknown;
  MustBeAlive: unknown;
}

/** both */
export interface LifeShieldUpdate {
  Id: number;
  Ratio: number;
}

/** unknown */
export interface LifeSpec {
  BurstDamageShield: unknown;
  DestroyOnDeath: unknown;
  DieMovementReduction: unknown;
  EffectToSpawnOnDeathId: unknown;
  Immunity: unknown;
  MaxLifePercentageDelayedPerSecond: unknown;
  NotACorpseWhenDead: unknown;
  RenegerationDelayAfterDamage: unknown;
  TargetableAfterDeathTime: unknown;
}

/** unknown */
export interface LifeStealBuffEffectSpec {
  RatioOfAttackDamage: unknown;
}

/** unknown */
export interface LifeforceBoostCommunityEvent {
  AttackIncreasedLifeForce: unknown;
  MineIncreasedLifeForce: unknown;
}

/** request */
export interface LimitedQuantityRewardItem {
  ShopSkusPack: unknown;
  LargeIconUrl: string;
  SmallIconUrl: string;
}

/** unknown */
export interface LineFieldSpec {
  EndLength: unknown;
  LocalStartOffsetX: unknown;
  LocalStartOffsetY: unknown;
  StartLength: unknown;
  Width: unknown;
}

/** unknown */
export interface LinearMoveInDirectionSpec {
  Distance: unknown;
  Orientation: unknown;
}

/** unknown */
export interface LinearMoveSpec {
  EaseInOut: unknown;
  Speed: unknown;
  Destination: unknown;
  OffsetDistanceToDestination: unknown;
}

/** unknown */
export interface LinearMoveToDestinationSpec {
  Destination: unknown;
  OffsetDistanceToDestination: unknown;
}

/** both */
export interface LinkedAccountResult {
  FacebookFriendsLinked: unknown;
  FacebookFriendsNotLinked: unknown;
  ReconnectUrl: string;
  RequireReconnect: boolean;
}

/** both */
export interface LinkedAccountResultModel {
  FacebookFriends: unknown;
}

/** both */
export interface LinkedAccountResultViewModel {
  FacebookFriendsLinked: unknown;
  FacebookFriendsNotLinked: unknown;
  ReconnectUrl: string;
  RequireReconnect: boolean;
}

/** unknown */
export interface LoadingScreenActiveAssignmentConditionSpec {
  AccountId: unknown;
}

/** unknown */
export interface LoadingScreenAssignmentActionSpec {
  Show: unknown;
}

/** unknown */
export interface LoadingScreenHiddenAssignmentTriggerSpec {
  GameEntityTypeMask: unknown;
}

/** both */
export interface LoadingScreenUpdatedEventArgs {
  LoadingBackgroundUrl: string;
  ShouldShow: boolean;
}

/** response */
export interface LoadingSettings {
  BackgroundImageUrlPrefix: string;
  LoadingCaptionOasisId: number;
}

/** both */
export interface LobbyBarModel {
  BuildNotificationsCount: number;
  GuildNotificationsCount: number;
  NewsNotificationCount: number;
  PendingFriendsCount: number;
  ProfileSummary: unknown;
  WalletSummary: unknown;
}

/** unknown */
export interface LocalSourceVectorSpec {
  Front: unknown;
  Right: unknown;
  Up: unknown;
}

/** both */
export interface LockButtonEventArgs {
  Button: number;
}

/** unknown */
export interface LockCameraAssignmentActionSpec {
  UnlockCamera: unknown;
}

/** unknown */
export interface LockCameraOrbitAssignmentActionSpec {
  OrbitDirectionMask: unknown;
}

/** unknown */
export interface LockWidgetsAssignmentActionSpec {
  AffectAllButtons: unknown;
  Buttons: unknown;
}

/** both */
export interface LoginResult {
  AccountId: number;
  ConnectionToken: string;
  ProfileId: string;
}

/** both */
export interface Loot {
  CreatureId: number;
  InventoryItem: InventoryItem;
  InventoryItemIndex: number;
  LootAmount: number;
  LootType: number;
  SourceEntityId: number;
  SourceEntityType: number;
}

/** unknown */
export interface LootCollectedAssignmentTriggerSpec {
  LootTypeMask: unknown;
}

/** both */
export interface LootModifierTable {
  Minus1Level: number;
  Minus2Levels: number;
  Minus3Levels: number;
  Minus4Levels: number;
  Minus5Levels: number;
  Plus1Level: number;
  Plus2Levels: number;
  Plus3Levels: number;
  Plus4Levels: number;
  Plus5Levels: number;
  Plus6Levels: number;
  SameLevel: number;
}

/** unknown */
export interface LootSelectionSpec {
  LootTypeMask: unknown;
}

/** unknown */
export interface LootSpec {
  Duration: unknown;
}

/** unknown */
export interface LootableSpec {
  DisableLoot: unknown;
  HealthOrbFragmentsLootBase: unknown;
  HealthOrbFragmentsLootPerLevel: unknown;
  LootDelayBetweenEachDrop: unknown;
  LootDropMaxDistance: unknown;
  LootDropMinDistance: unknown;
  LootDropSectorCircleArc: unknown;
  LootDropSectorCircleArcStartAngle: unknown;
  LootRadius: unknown;
  OverrideAttackSettingsLootConfig: unknown;
  PVEDroppableLootTypeMask: unknown;
  PVEForceDropLootTypeMask: unknown;
  PVPDroppableLootTypeMask: unknown;
  PVPForceDropLootTypeMask: unknown;
  SpecialLootChance: unknown;
  SpecialLootTable: unknown;
}

/** both */
export interface LootedHeroItemParam {
  ItemId: number;
  ItemIndex: number;
}

/** both */
export interface LoseTrophyCooldownRemainingTimeUpdatedEventArgs {
  LoseTrophyCooldownRemainingTime: number;
}

/** both */
export interface LossPonderation {
  AttackCastlePercentageLoss: number;
  AttackerDefenderLevelDiff: number;
  ShieldDuration: number;
}

/** unknown */
export interface MagicFindBoostCommunityEvent {
  IncreasedChance: unknown;
}

/** request */
export interface MagicFindBoostConsumableTemplate {
  IncreasedChance: number;
}

/** both */
export interface MagicalPropertiesReplacementPreference {
  ReplacedDebugName: string;
  ReplacedEffect: unknown;
  ReplacementEffects: unknown;
}

/** both */
export interface MagicalPropertyModel {
  ChanceToLevelUp: number;
  Comparison: number;
  FormatValueAsPercentage: boolean;
  FormatValuePrecision: number;
  FormatWithPlusSign: number;
  Icon: string;
  Id: number;
  IsMagicalPropertyMaxedOut: boolean;
  IsMagicalPropertyMaxedOutForItemLevel: boolean;
  Level: number;
  LevelReplacementIcon: string;
  LevelUpText: string;
  Name: string;
  OasisDescription: number;
  Type: number;
  Value: number;
}

/** request */
export interface MaintenanceGlobalNotification {
  MaintenanceScheduledDate: string;
  MaintenanceScheduledInSeconds: number;
}

/** unknown */
export interface ManaOperationSpec {
  Value: unknown;
}

/** both */
export interface Match {
  Length: number;
  Locale: string;
  Matched: string;
  Quantity: number;
  Root: string;
  Severity: string;
  Start: number;
  Tags: unknown;
  Type: string;
}

/** unknown */
export interface MaterialMineBoostCommunityEvent {
  MineProductionPeriodModifier: unknown;
  iner: unknown;
}

/** both */
export interface MaterialsCountByQualityList {
  Count: number;
  Qualities: unknown;
}

/** unknown */
export interface MaxValueSpec {
  Value1: unknown;
  Value2: unknown;
}

/** unknown */
export interface MeleeOperationSpec {
  MaxDistance: unknown;
  ObstacleCollisionHeight: unknown;
  ObstacleCollisionMaskAll: unknown;
  ObstacleCollisionMaskAny: unknown;
  Operations: unknown;
  ShiftAttackDistance: unknown;
  ShiftAttackRadius: unknown;
}

/** both */
export interface MemoryInfoTracking {
  ClockFrequencyHz: number;
  MemoryTypeName: string;
  TotalBytes: number;
}

/** both */
export interface Message {
  Data: unknown;
  DateSent: string;
  SenderId: number;
  Type: number;
}

/** request */
export interface MessageBoxAssignmentActionSpec {
  ButtonPressedAfterTimer: number;
  ControllerName: string;
  HasTimer: boolean;
  Height: number;
  HideNavigation: boolean;
  Id: number;
  IsCloseButtonVisible: boolean;
  IsModal: boolean;
  OffsetBottom: number;
  OffsetLeft: number;
  OffsetRight: number;
  OffsetTop: number;
  Position: number;
  PositionElementId: string;
  Submenu: string;
  Text: string;
  TimeBeforeClosing: number;
  Title: string;
  Type: number;
  Width: number;
}

/** both */
export interface MessageBoxClosedEventArgs {
  ButtonClicked: number;
  Id: number;
}

/** both */
export interface MessageBoxEventArgs {
  MessageBoxOption: unknown;
}

/** both */
export interface MessageBoxInformation {
  ButtonPressedAfterTimer: number;
  HasTimer: boolean;
  Id: number;
  MessageBoxButtonConfig: number;
  MessageOasisId: number;
  TimeBeforeClosing: number;
  TitleOasisId: number;
}

/** request */
export interface MessageBoxPanelNavigationModel {
  IsOpalPanel: boolean;
  MessageBoxOption: unknown;
  PanelName: number;
}

/** unknown */
export interface MessageBoxSettings {
  MessageBoxes: unknown;
}

/** request */
export interface MessageNotification {
  Sender: number;
  ThreadId: number;
}

/** both */
export interface MessagePreview {
  Data: unknown;
  Type: number;
}

/** both */
export interface MessagingSettings {
  HasEmailNotification: boolean;
}

/** unknown */
export interface MinValueSpec {
  Value1: unknown;
  Value2: unknown;
}

/** both */
export interface MineBuildingDestructibleStateChangedEventArgs {
  BuildingId: number;
  IsDestroyed: boolean;
}

/** request */
export interface MineBuildingInfoDataModel {
  CurrentCapacity: number;
  CurrentHealth: number;
  CurrentProductionRate: number;
  HasMultipleRanks: boolean;
  MaxCapacity: number;
  MaxHealth: number;
  MaxProductionRate: number;
  ProductionPeriodInHours: number;
  ProductionPeriodInMinutes: number;
  ProductionPeriodInSeconds: number;
}

/** unknown */
export interface MineBuildingRankSpec {
  AutomaticProduction: unknown;
  Capacity: unknown;
  InitialLevel: unknown;
  LevelProductionPacks: unknown;
  ProductionPeriod: unknown;
  ProductionValue: unknown;
  QualityChance: unknown;
}

/** unknown */
export interface MineBuildingSpec {
  CurrencyType: unknown;
  InitialAmount: unknown;
}

/** request */
export interface MineBuildingUpgradePopupDataModel {
  NewCapacity: number;
  NewHealth: number;
  NewProductionRate: number;
}

/** both */
export interface MineCount {
  Count: number;
  MineFieldIngredientId: number;
}

/** request */
export interface MineEnabledNotification {
  CastleBuildingId: number;
  ProductionExpirableId: string;
  Index: number;
  NotificationType: number;
}

/** both */
export interface MineHarvestHoverEventArgs {
  MineHarvestHoverModel: MineHarvestHoverModel;
}

/** request */
export interface MineHarvestHoverModel {
  IsStorageFull: boolean;
  MineDisplayName: string;
  MineMaxCapacity: number;
  MineRank: number;
  MineSpecContainerId: number;
}

/** request */
export interface MinePillagedNotification {
  CastleBuildingId: number;
  Destroyed: boolean;
  ShieldExpirableId: string;
  StolenAmount: number;
}

/** both */
export interface MineProductionCompletedEventArgs {
  MineProductionCompletedInfosModel: MineProductionCompletedInfosModel;
}

/** both */
export interface MineProductionCompletedInfosModel {
  BuildingId: number;
  BuilingSpecContainerId: number;
  ProductionAdded: number;
}

/** request */
export interface MineProductionCompletedNotification {
  BuildingId: number;
  InventoryItemAdded: unknown;
  NextProductionExpirableId: string;
  ProductionAdded: number;
  ProductionLevel: number;
}

/** request */
export interface MineProductionExpirable {
  BuildingId: number;
  ExpirableType: number;
  ProductionValue: number;
}

/** both */
export interface MineProductionRemainingTimeUpdatedEventArgs {
  EntityHarvestId: number;
  EntityHarvestType: number;
  ProductionLevel: number;
  ProductionLevelMax: number;
  RemainingTime: number;
}

/** request */
export interface MineProductionStartedNotification {
  BuildingId: number;
  NextProductionExpirableId: string;
  ProductionLevel: number;
}

/** both */
export interface MineShieldAddedEventArgs {
  BuildingId: number;
  ShieldRemainingTime: number;
}

/** request */
export interface MineShieldExpirable {
  BuildingId: number;
  ExpirableType: number;
}

/** request */
export interface MineShieldExpiredNotification {
  CastleBuildingId: number;
  ExpirableId: string;
}

/** both */
export interface MineStatus {
  CumulatedAmount: number;
  CumulatedHeroItems: unknown;
  IsActive: boolean;
  IsDestroyed: boolean;
  ProductionExpirableId: string;
  Productionlevel: number;
  ShieldExpirableId: string;
}

/** request */
export interface MineTimeBonusPanelNavigationModel {
  TimeBonus: number;
}

/** unknown */
export interface MissileSpawnOperationSpec {
  ArcAngle: unknown;
  ArcOffset: unknown;
  BurstDelay: unknown;
  BurstsAngle: unknown;
  BurstsCount: unknown;
  CancelSpawningWhenWallBetweenOwnerAndSpawnPos: unknown;
  DivideBurstDelayByNumberOfDelays: unknown;
  FirstBurstOffset: unknown;
  IsBurstsOrderRandomized: unknown;
  IsFirstBurstDelayed: unknown;
  Missile: unknown;
  MissilesCount: unknown;
  MovementTarget: unknown;
  SpawnPosition: unknown;
  TargetPosition: unknown;
}

/** unknown */
export interface MissileSpec {
  CanBeAfterAggroActivity: unknown;
  Movement: unknown;
}

/** unknown */
export interface MissileSpecContainer {
  Type: unknown;
  SpecContainerReferenceId: unknown;
}

/** unknown */
export interface MissileSpecContainerRef {
  SpecContainerReferenceId: unknown;
}

/** unknown */
export interface ModifiedLootCommunityEvent {
  ItemDropByType: unknown;
}

/** unknown */
export interface MouseDragEndedAssignmentTriggerSpec {
  ButtonIndex: unknown;
}

/** unknown */
export interface MoveCollisionSpec {
  CheckCollision: unknown;
  CheckCollisionBetweenCasterAndEntityAtStart: unknown;
  CheckDeadCollision: unknown;
  CollisionAllianceFilter: unknown;
  CollisionCountBeforeStop: unknown;
  CollisionMask: unknown;
  CollisionShape: unknown;
  OnContinuousCollisionOperations: unknown;
  OnEnteringCollisionOperations: unknown;
  OnFirstEnteredCollisionOperations: unknown;
  OnStopperCollisionOperations: unknown;
  StopperCollisionMask: unknown;
  StopperCollisionShape: unknown;
  TrajectorySlideMaxAngle: unknown;
  TrajectorySlideRedirectionDelay: unknown;
}

/** unknown */
export interface MoveOperationSpec {
  Movement: unknown;
}

/** unknown */
export interface MoveSpec {
  CanExitNavMesh: unknown;
  Collision: unknown;
  ForceNewMoveInsteadOfReEnteringSameOne: unknown;
  IgnoreMissileParamsIfAny: unknown;
  IgnoreMovementReduction: unknown;
  IgnoreResistance: unknown;
  KnockbackSpec: unknown;
  MoveStyle: unknown;
  OnMoveOperations: unknown;
  OnStopOperations: unknown;
}

/** unknown */
export interface MoveStyleSpec {
  Booleans: unknown;
}

/** unknown */
export interface MovementSpec {
  CanMove: unknown;
}

/** both */
export interface MovementSpeed {
  Id: number;
  Name: unknown;
  SpeedFrom: number;
  SpeedTo: number;
}

/** unknown */
export interface MultValueSpec {
  Value1: unknown;
  Value2: unknown;
}

/** unknown */
export interface MultVectorSpec {
  Value1: unknown;
  Value2: unknown;
}

/** unknown */
export interface MultiConditionsValueItemSpec {
  Comparaison: unknown;
  Value: unknown;
}

/** unknown */
export interface MultiConditionsValueSpec {
  Values: unknown;
}

/** both */
export interface MultiPanelNavigationModel {
  Models: unknown;
}

/** both */
export interface MultiplePriceTooltipModel {
  Amounts: unknown;
  IsAffordable: boolean;
}

/** both */
export interface MyRankingModel {
  Country: Country;
  RankInCountry: number;
  RankInFriends: number;
  RankInWorld: number;
  RankInZone: number;
  Zone: Zone;
}

/** unknown */
export interface NameSpec {
  P0Z: unknown;
  DebugName: unknown;
  OasisDescription: unknown;
  OasisName: unknown;
}

/** both */
export interface NamedItemEffectLevelUnlock {
  MaxEffectLevel: number;
  MinItemLevel: number;
}

/** both */
export interface NamedItemPowerUpLevelUnlock {
  MaxPowerUpLevel: number;
  MinItemLevel: number;
}

/** both */
export interface NarrativeVoTextPage {
  Text: string;
  TextOasisId: number;
  Vo: unknown;
}

/** request */
export interface NavBarPanelNavigationModel {
  CrownsCount: number;
  HeroID: number;
  HeroLevel: number;
  IconLayerName: string;
  IsAttackDefenseVisible: boolean;
  IsInAttackSelection: boolean;
  NextLevelXp: number;
  PanelName: number;
  WalletSummaryModel: WalletSummaryModel;
  Xp: number;
}

/** unknown */
export interface NavigationGridMemberSpec {
  ObstacleShape: unknown;
  ObstacleType: unknown;
}

/** unknown */
export interface NavigationGridObstacleCircleShapeSpec {
  Radius: unknown;
}

/** unknown */
export interface NavigationGridObstacleShapeSpec {
  Booleans: unknown;
}

/** response */
export interface NavigationSettings {
  AttractionMaxSpeedRatio: number;
  DefaultMinimumNavigationSpeed: number;
  DefaultTimeToReachFullSpeed: number;
  FlockingSeparationWeight: number;
  MaxRepulsiveSpeed: number;
  RepathDelay: number;
  SeparationAndInterpenetrationAwarenessRadius: number;
  UseMinimumNavigationSpeed: boolean;
}

/** unknown */
export interface NavigationSpec {
  GroupsToAvoidMask: unknown;
  MinimumSpeed: unknown;
  NavigationAvoidanceMask: unknown;
  NeedToFaceTargetBeforeMoving: unknown;
  OverrideDefaultMinimumSpeed: unknown;
  OverrideDefaultTimeToReachFullSpeed: unknown;
  PenetrationRadius: unknown;
  RepathDelay: unknown;
  SeparationDistance: unknown;
  SimplifyPathEachFrame: unknown;
  StartSpeedBoost: unknown;
  TargetUnreachableMovementTolerance: unknown;
  TimeToReachFullSpeed: unknown;
  UpdateTargetPositionDelay: unknown;
}

/** request */
export interface NavigationTracking {
  GameUrl: string;
}

/** unknown */
export interface NbCurrencyClustersToDropOnDiedLevelSpec {
  MaxDestructibleLevel: unknown;
  NbCurrencyClustersToDropOnDied: unknown;
}

/** both */
export interface NearDeathFxInfo {
  Fx: unknown;
  Threshold: number;
}

/** request */
export interface News {
  Data: unknown;
  Id: string;
  IsUnread: boolean;
  Priority: number;
  PublishDate: string;
}

/** request */
export interface NewsAddedNotification {
  NewsItem: unknown;
}

/** both */
export interface NewsCategorySettings {
  Priority: number;
  Type: number;
}

/** both */
export interface NewsChangedEventArgs {
  News: News;
  UnreadCount: number;
}

/** both */
export interface NewsData {
  IsMaintained: boolean;
  IsPromoted: boolean;
  LeagueId: number;
  LeagueRank: number;
  SubLeagueId: number;
  SubLeagueName: string;
  SubLeaguePrefixName: string;
  SubLeagueSmallIconUrl: string;
}

/** both */
export interface NewsResult {
  LastViewedNewsId: string;
  News: News;
}

/** unknown */
export interface NewsSettings {
  NewsCategories: unknown;
  NewsMaxCount: unknown;
  NewsTimeout: unknown;
}

/** both */
export interface NewsViewModel {
  AvatarUrl: string;
  IsCastleAttackable: boolean;
  News: News;
  SpecialPackModel: SpecialPackModel;
}

/** request */
export interface NoHeroDeathCondition {
  DebugName: string;
  OasisId: number;
}

/** both */
export interface Notification {
  AttackId: string;
  CastleRating: number;
  Message: Message;
}

/** both */
export interface OSInfoTracking {
  Is64Bit: boolean;
  IsoRegionalCode: string;
  Name: string;
  ServicePack: number;
}

/** response */
export interface Objective {
  Category: number;
  ClientSideCompletion: boolean;
  Conditions: number;
  DebugName: string;
  Description: number;
  IconUrl: string;
  Id: number;
  Instruction: number;
  ManualPopupTriggerOnCompletion: boolean;
  PerHeroReward: unknown;
  Progression: number;
  Requirements: number;
  Reward: number;
  ShowUnlockedPopup: boolean;
  Title: number;
  VoiceOverSoundId: string;
}

/** both */
export interface ObjectiveActivatedEventArgs {
  Conditions: unknown;
  Description: number;
  LayerName: string;
  ObjectiveId: number;
}

/** unknown */
export interface ObjectiveCompletedAssignmentTriggerSpec {
  ObjectiveId: unknown;
}

/** both */
export interface ObjectiveCompletedEventArgs {
  CompletedObjectiveId: number;
  UnlockedObjectives: unknown;
}

/** request */
export interface ObjectiveCompletedNotification {
  ObjectiveId: number;
}

/** request */
export interface ObjectiveCompletedObjectiveRequirement {
  ObjectiveId: number;
}

/** request */
export interface ObjectiveCompletedPanelNavigationModel {
  Description: string;
  ExcludeModalPopupOpening: boolean;
  Id: number;
  IsOpalPanel: boolean;
  PanelName: number;
  Reward: Reward;
  RewardXp: number;
  Title: string;
}

/** both */
export interface ObjectiveCondition {
  DebugName: string;
  OasisId: number;
}

/** both */
export interface ObjectiveConditionModel {
  ConditionId: number;
  Description: string;
  Progression: number;
  ProgressionTarget: number;
  Status: number;
}

/** both */
export interface ObjectiveConditionUpdatedEventArgs {
  Condition: unknown;
  ObjectiveId: number;
}

/** both */
export interface ObjectiveEntryModel {
  Category: number;
  Conditions: unknown;
  Description: string;
  HasAudioPlayed: boolean;
  HasViewed: boolean;
  HeroSpecContainerId: number;
  IconUrl: string;
  Id: number;
  IsFailed: boolean;
  Progression: unknown;
  Reward: Reward;
  Status: number;
  Title: string;
  Type: number;
}

/** request */
export interface ObjectiveListPanelNavigationModel {
  IsOpalPanel: boolean;
  PanelName: number;
}

/** both */
export interface ObjectiveListUpdatedEventArgs {
  UnlockedObjectives: unknown;
}

/** both */
export interface ObjectivePopupClosedEventArgs {
  ObjectiveEntryModel: ObjectiveEntryModel;
}

/** request */
export interface ObjectivePopupPanelNavigationModel {
  ActionButtonModel: ActionButtonModel;
  Conditions: unknown;
  Description: string;
  ExcludeModalPopupOpening: boolean;
  IconLayerName: string;
  IsCompleted: boolean;
  IsFailed: boolean;
  IsNew: boolean;
  IsOpalPanel: boolean;
  ObjectiveId: number;
  PanelName: number;
  Reward: Reward;
  Title: string;
  VoiceOverSoundId: string;
}

/** response */
export interface ObjectiveProgression {
  Total: number;
}

/** both */
export interface ObjectiveProgressionModel {
  Current: number;
  Total: number;
}

/** request */
export interface ObjectiveProgressionUpdatedNotification {
  NewCount: number;
  ObjectiveId: number;
}

/** request */
export interface ObjectiveRequirement {
  AttackRegionId: number;
}

/** unknown */
export interface ObjectiveSettings {
  DisplayableMaxCount: unknown;
  Objectives: unknown;
}

/** both */
export interface ObjectiveSummaryEntryModel {
  Category: number;
  Description: string;
  IconUrl: string;
  Id: number;
  Instruction: string;
  Reward: Reward;
  Title: string;
  Type: number;
}

/** request */
export interface ObjectiveUnlockCommand {
  ObjectiveId: number;
}

/** unknown */
export interface ObjectiveUnlockedAssignmentTriggerSpec {
  ObjectiveId: unknown;
}

/** both */
export interface ObjectiveUnlockedEventArgs {
  UnlockedObjective: unknown;
  UnlockedObjectives: unknown;
}

/** request */
export interface ObjectiveUnlockedNotification {
  AccountObjective: AccountObjective;
}

/** both */
export interface ObjectiveViewedCommand {
  ObjectiveId: number;
}

/** unknown */
export interface ObjectivesCompletedAssignmentConditionSpec {
  Objectives: unknown;
}

/** unknown */
export interface ObstacleSpec {
  DestroyWhenRemovingObstacle: unknown;
  Duration: unknown;
  Height: unknown;
  InternalShapesNumber: unknown;
  InternalShapeType: unknown;
  Offset: unknown;
  RemoveObstacleOnDied: unknown;
  Thickness: unknown;
  Width: unknown;
}

/** unknown */
export interface OnBuffStoppedBuffEffectSpec {
  p2Z: unknown;
  Operations: unknown;
}

/** unknown */
export interface OnCurrentAbilityChangedBuffEffectSpec {
  IsAttackAbilitySlotIndexExcluded: unknown;
  IsNotInNewAbilitySpecContainerIds: unknown;
  NewAbilitySpecContainerIds: unknown;
  Operations: unknown;
}

/** unknown */
export interface OnDamageBuffEffectSpec {
  IgnoreReflectedDamage: unknown;
  IgnoreSelfInflictedDamage: unknown;
  MustBeBasicAttackDamage: unknown;
  Operations: unknown;
  OperationsCooldown: unknown;
  OperationsCountLimitation: unknown;
  OperationTypeFilter: unknown;
  Target: unknown;
  TargetTypeFilter: unknown;
}

/** unknown */
export interface OnDamageReceivedBuffEffectSpec {
  Operations: unknown;
  OperationTypeFilter: unknown;
  Target: unknown;
}

/** unknown */
export interface OnDeathBuffEffectSpec {
  Delay: unknown;
  Operations: unknown;
}

/** unknown */
export interface OnEntityAggroedBuffEffectSpec {
  Operations: unknown;
}

/** unknown */
export interface OnKillBuffEffectSpec {
  Operations: unknown;
}

/** unknown */
export interface OnLifeChangedBuffEffectSpec {
  MaxLife: unknown;
  MinLife: unknown;
  OnEnterIntervalOperations: unknown;
  OnExitIntervalOperations: unknown;
}

/** unknown */
export interface OnMissileExplodedBuffEffectSpec {
  Operations: unknown;
}

/** unknown */
export interface OnMissileLaunchedBuffEffectSpec {
  FilteringList: unknown;
  IsFilteringListInclusive: unknown;
  Operations: unknown;
}

/** unknown */
export interface OnNavigationStartedBuffEffectSpec {
  Operations: unknown;
}

/** unknown */
export interface OnOtherBuffAddedBuffEffectSpec {
  BuffSpecContainerIds: unknown;
  Operations: unknown;
}

/** unknown */
export interface OnSpellTriggerExecuteOperationBuffEffectSpec {
  Operations: unknown;
}

/** unknown */
export interface OnTickBuffEffectSpec {
  Interval: unknown;
  IsExecutedOnEnter: unknown;
  Operations: unknown;
}

/** request */
export interface OpenPanelAssignmentActionSpec {
  IsOpalPanel: boolean;
  PanelName: string;
  TargetEntitySearch: unknown;
}

/** both */
export interface OpenWebBrowserEventArgs {
  CloseButtonLeft: number;
  CloseButtonTop: number;
  HideBlackOverlay: boolean;
  SetCloseButtonPosition: boolean;
  ShowBlackOverlay: boolean;
}

/** unknown */
export interface OperationAbilityLevelSpec {
  Operations: unknown;
}

/** unknown */
export interface OperationListenerConditionSpec {
  ListenedOperationSourceTypeFlags: unknown;
  Operation: unknown;
}

/** unknown */
export interface OperationListenerSpec {
  OperationListerners: unknown;
}

/** unknown */
export interface OperationSpec {
  Target: unknown;
  ArcAngle: unknown;
  ArcOffset: unknown;
  BurstDelay: unknown;
  BurstsAngle: unknown;
  BurstsCount: unknown;
  CancelSpawningWhenWallBetweenOwnerAndSpawnPos: unknown;
  DivideBurstDelayByNumberOfDelays: unknown;
  FirstBurstOffset: unknown;
  IsBurstsOrderRandomized: unknown;
  IsFirstBurstDelayed: unknown;
  Missile: unknown;
  MissilesCount: unknown;
  MovementTarget: unknown;
  SpawnPosition: unknown;
  TargetPosition: unknown;
}

/** unknown */
export interface OperationTargetSpec {
  Type: unknown;
}

/** request */
export interface OptionControlSchemePanelNavigationModel {
  GameStateType: number;
}

/** both */
export interface OptionGamePlayModel {
  AutoFireOnDirectModeEnabled: boolean;
  LootCollectorFilterEnabled: boolean;
  ProfanityFilterEnabled: boolean;
  StopContinuousMoveOnClickReleaseEnabled: boolean;
  UseCameraDampingEnabled: boolean;
}

/** both */
export interface OptionInformation {
  Category: number;
  OasisId: number;
}

/** request */
export interface OptionModel {
  GamePlay: unknown;
  Sound: unknown;
  Video: unknown;
}

/** request */
export interface OptionPanelNavigationModel {
  IsOpalPanel: boolean;
  OptionViewModel: OptionViewModel;
  Tab: number;
}

/** both */
export interface OptionParameterBaseModel {
  Interval: number;
  MaxValue: number;
  MinValue: number;
  Type: number;
  Value: number;
  ValueToRoundDisplayValue: number;
}

/** request */
export interface OptionParameterCheckboxModel {
  IsChecked: boolean;
  Type: number;
}

/** request */
export interface OptionParameterComboboxModel {
  SelectedKey: number;
  Type: number;
  Values: unknown;
}

/** request */
export interface OptionParameterSliderModel {
  Interval: number;
  MaxValue: number;
  MinValue: number;
  Type: number;
  Value: number;
  ValueToRoundDisplayValue: number;
}

/** unknown */
export interface OptionSettings {
  AntiAliasingType: unknown;
  AutoDetectedOasisId: unknown;
  BackgroundFPSSlider: unknown;
  CaptionCustomScreenSizeOasisId: unknown;
  CaptionOffOasisId: unknown;
  CaptionOnOasisId: unknown;
  ConfigType: unknown;
  ConfigurationOasisId: unknown;
  CustomConfigurationOasisId: unknown;
  EnableAmbienceOasisId: unknown;
  EnableMusicOasisId: unknown;
  EnableSfxOasisId: unknown;
  EnableVoiceOasisId: unknown;
  FilteringType: unknown;
  ForegroundFPSSlider: unknown;
  FXAAType: unknown;
  GammaSlider: unknown;
  GeneralVolumeOasisId: unknown;
  Quality: unknown;
  RenderingScaleSlider: unknown;
  ShadowConfigurationOasisId: unknown;
  VolumeSlider: unknown;
  WindowType: unknown;
}

/** both */
export interface OptionSoundModel {
  EnableAmbienceText: string;
  EnableMusicText: string;
  EnableSfxText: string;
  EnableVoiceText: string;
  GeneralVolumeText: string;
  VolumeCoef: number;
}

/** both */
export interface OptionValueChangedEventArgs {
  EnableSave: boolean;
  HasSavedOnce: boolean;
}

/** both */
export interface OptionValueModel {
  Key: number;
  Value: string;
}

/** request */
export interface OptionVideoApplyPanelNavigationModel {
  IsClosingOptionPanel: boolean;
  IsOpalPanel: boolean;
  PanelName: number;
}

/** both */
export interface OptionVideoModel {
  AdvancedParameters: unknown;
  BasicParameters: unknown;
  Configurations: unknown;
}

/** both */
export interface OptionViewModel {
  AudioAmbienceEnable: boolean;
  AudioMasterVolumeRatio: number;
  AudioMusicEnable: boolean;
  AudioSfxEnable: boolean;
  AudioVoiceEnable: boolean;
  AutoFireOnDirectModeEnabled: boolean;
  CurrentQuality: number;
  DefaultLevel: number;
  Distortion: boolean;
  EnableAmbienceText: string;
  EnableMusicText: string;
  EnableSfxText: string;
  EnableVoiceText: string;
  Fog: boolean;
  FPSClamping: number;
  FPSClampingNoFocus: number;
  FXAA: number;
  Gamma: number;
  GeneralVolumeText: string;
  Glow: boolean;
  LensFlare: boolean;
  MinHeroItemQualityToPickUp: number;
  ObjectComplexity: number;
  PostEffects: boolean;
  ProfanityFilterEnabled: boolean;
  RenderQuality: number;
  ScreenSize: number;
  Shadows: number;
  SSAO: number;
  StopContinuousMoveOnClickReleaseEnabled: boolean;
  UseCameraDampingEnabled: boolean;
  UseTopFrustumOnly: boolean;
  VolumeCoef: number;
  VSync: boolean;
  WindowType: number;
}

/** both */
export interface OptionViewModelChangedEventArgs {
  OptionViewModel: OptionViewModel;
}

/** unknown */
export interface OrBooleanSpec {
  Booleans: unknown;
}

/** unknown */
export interface OrbSpec {
  Value: unknown;
}

/** unknown */
export interface OrientationSpec {
  SaveOrientationSlot: unknown;
}

/** both */
export interface OrientedSpawnPosition {
  Orientation: number;
  Orientation: number;
  Orientation: number;
}

/** unknown */
export interface OrientedVectorSpec {
  Orientation: unknown;
  Value: unknown;
}

/** unknown */
export interface OverrideCameraOcclusionFlagsAssignmentActionSpec {
  Enable: unknown;
  ShowWalls: unknown;
}

/** response */
export interface PackageAsset {
  ResourcePath: number;
}

/** response */
export interface PackageContent {
  Assets: number;
  PackageName: string;
}

/** response */
export interface PackageContentCollection {
  Packages: number;
}

/** both */
export interface PackageVersionInfoIdTracking {
  PackageName: string;
  Type: number;
}

/** unknown */
export interface PanAttackSelectionCameraAssignmentActionSpec {
  Pitch: unknown;
  Yaw: unknown;
}

/** unknown */
export interface PanelClosedAssignmentTriggerSpec {
  PanelName: unknown;
}

/** both */
export interface PanelNamesListEventArgs {
  CurrentAbsoluteTimeInSeconds: number;
  PanelNamesList: unknown;
}

/** both */
export interface PanelNavigationEventArgs {
  CurrentAbsoluteTimeInSeconds: number;
  GameEntityID: number;
  PanelId: string;
  PanelNavigationModel: PanelNavigationModel;
}

/** both */
export interface PanelNavigationModel {
  RewardModel: RewardModel;
}

/** unknown */
export interface PanelNotShownAssignmentConditionSpec {
  PanelName: unknown;
}

/** both */
export interface PanelSettings {
  ContainerControls: unknown;
  ContainerFilename: number;
  IconOffset3D: unknown;
  PanelLayer: number;
  SpecificZoomSettings: unknown;
  SubContainerFilenames: unknown;
  TooltipContainers: unknown;
  UseHeadNode: boolean;
  ZBias: number;
}

/** unknown */
export interface PanelShownAssignmentConditionSpec {
  PanelName: unknown;
}

/** unknown */
export interface PanelShownAssignmentTriggerSpec {
  PanelName: unknown;
  ParameterName: unknown;
  ParameterValue: unknown;
}

/** both */
export interface PanelSoundPresets {
  ActivationPresets: unknown;
  DeactivationPresets: unknown;
}

/** both */
export interface PanelSoundPresetsSettings {
  SoundPresetsByPanel: unknown;
}

/** request */
export interface PanelTracking {
  OpenCloseDurationInseconds: number;
  Panel: number;
}

/** both */
export interface PanelVisibilityInformation {
  CastleRenovationLevel: number;
  PanelName: number;
}

/** unknown */
export interface ParentingSpec {
  Children: unknown;
}

/** unknown */
export interface PatchingSettings {
  PercentScrollName: unknown;
  PercentTextName: unknown;
  StatusTextName: unknown;
}

/** request */
export interface PausePanelNavigationModel {
  DisableLeaveCastle: boolean;
  DisableRestartCastle: boolean;
  IsAttack: boolean;
  IsRevengeAttack: boolean;
}

/** request */
export interface PcConfigurationTracking {
  AudioInfo: unknown;
  CPUInfo: unknown;
  DiskInfo: unknown;
  GraphicsInfo: unknown;
  MemoryInfo: unknown;
  OSInfo: unknown;
  CreationDate: string;
  TrackingTagId: number;
}

/** both */
export interface PendingRegionsChangedViewModel {
  UpdatedAttackRegions: unknown;
}

/** both */
export interface Period {
  EndDateTime: string;
  StartDateTime: string;
}

/** both */
export interface PetScaleInfo {
  CreatureId: number;
  Scale: number;
}

/** unknown */
export interface PetSpawnableEntitySpec {
  TemplateId: unknown;
}

/** unknown */
export interface PetSpec {
  AttractableLootTypeMask: unknown;
}

/** unknown */
export interface PhysicSpec {
  CollisionGroup: unknown;
  CreateShapesFromNodes: unknown;
  PhysicRigidBodyType: unknown;
  Radius: unknown;
  Shapes: unknown;
}

/** unknown */
export interface PickingSettings {
  GameEntityTypePriorities: unknown;
}

/** unknown */
export interface PickingSpec {
  ForceAttackPickingFlags: unknown;
  ForceBuildPickingFlags: unknown;
  IsActivatedInAttack: unknown;
  ManualActivationOnInit: unknown;
  MeshAlignedBoxCapsuleHeightMultiplier: unknown;
  OuterShapes: unknown;
  PickingPriorityOverrride: unknown;
  PickingShapeSizeMultiplierWhenMoving: unknown;
  Shapes: unknown;
  UseMeshAlignedBoxCapsule: unknown;
}

/** unknown */
export interface PieSliceFieldSpec {
  PieSliceEndAngle: unknown;
  PieSliceStartAngle: unknown;
}

/** both */
export interface PillagedMine {
  CastleBuildingId: number;
  IsDestroyed: boolean;
  StolenAmount: number;
  StolenHeroItems: unknown;
}

/** unknown */
export interface PivotRotationMoveSpec {
  AngularSpeed: unknown;
  PivotPosition: unknown;
  RotationAngle: unknown;
}

/** request */
export interface PlayGameClickedTracking {
  Platform: number;
  CreationDate: string;
  TrackingTagId: number;
}

/** request */
export interface PlayMovieAssignmentActionSpec {
  IsMovieSkippable: boolean;
  MovieFile: string;
}

/** request */
export interface PlaySoundEventAssignmentActionSpec {
  SoundEvent: unknown;
}

/** both */
export interface PlayerInteractionModel {
  AccountDisplayName: string;
  AccountId: number;
  AttackSource: number;
  CastleType: number;
  IsAddFriendVisible: boolean;
  IsAttackVisible: boolean;
  IsCastleAttackable: boolean;
  IsChallengeVisible: boolean;
  IsFriend: boolean;
  IsGuildKickOutVisible: boolean;
  IsGuildPromoteAsLeader: boolean;
  IsGuildRecruitVisible: boolean;
  IsIgnoreVisible: boolean;
}

/** both */
export interface PlayerInteractionParams {
  AttackSource: number;
  IsAddFriendVisible: boolean;
  IsAttackVisible: boolean;
  IsChallengeVisible: boolean;
  IsIgnoreVisible: boolean;
}

/** both */
export interface PlayerLoadConfig {
  HeroSpecContainerId: number;
}

/** request */
export interface PopUpNarrativeVoTextPagesSpec {
  NarrativeVoTextPages: NarrativeVoTextPage;
}

/** request */
export interface PopupAssignmentActionSpec {
  ActionName: string;
  ArrowDirection: number;
  ArrowPosition: number;
  ControllerName: string;
  GameButtonId: number;
  HideOverlay: boolean;
  Id: string;
  InventoryItemDefinition: unknown;
  IsCloseButtonVisible: boolean;
  Left: number;
  NarrativePictureUrl: string;
  OffsetLeft: number;
  OffsetTop: number;
  OverlayAlpha: number;
  ParentContainer: string;
  PopupBindingVariable: string;
  PopUpNarrativeVoTextPages: unknown;
  Position: number;
  PositionElementId: string;
  ShopItemDefinition: unknown;
  ShowOverlay: boolean;
  StaticScreenText: string;
  StaticScreenTextOasisId: number;
  TargetEntitySearch: unknown;
  Text: string;
  TextAnimationCharsDelayScale: number;
  TextAnimationDelay: number;
  TextAnimationDuration: number;
  TextAnimationEffect: string;
  TextOasisId: number;
  Title: string;
  TitleOasisId: number;
  Top: number;
  Type: number;
}

/** unknown */
export interface PopupClosedAssignmentTriggerSpec {
  ButtonClicked: unknown;
  Id: unknown;
}

/** both */
export interface PopupClosedEventArgs {
  ButtonClicked: number;
  Id: string;
}

/** both */
export interface PopupEventArgs {
  PopupOption: unknown;
}

/** request */
export interface PopupOnTargetAssignmentActionSpec {
  Direction: number;
  LocalOffset: unknown;
  Selections: unknown;
  Type: number;
  ViewOffsetX: number;
  ViewOffsetY: number;
}

/** request */
export interface PopupOptionsModel {
  ArrowDirection: number;
  ArrowPosition: number;
  GameButtonId: number;
  GameEntityId: number;
  HideOverlay: boolean;
  Id: string;
  InventoryItemDefinition: unknown;
  IsCloseButtonVisible: boolean;
  IsOpalPanel: boolean;
  Left: number;
  NarrativePictureUrl: string;
  OffsetLeft: number;
  OffsetTop: number;
  OverlayAlpha: number;
  PanelName: number;
  ParentContainer: string;
  PopupBindingVariable: string;
  Position: number;
  PositionElementId: string;
  ShopItemDefinition: unknown;
  ShowOverlay: boolean;
  StaticScreenText: string;
  Text: string;
  TextAnimationCharsDelayScale: number;
  TextAnimationDelay: number;
  TextAnimationDuration: number;
  TextAnimationEffect: string;
  Texts: unknown;
  Title: string;
  Top: number;
  Type: number;
}

/** both */
export interface PopupShowMoreTextEventArgs {
  Id: string;
}

/** unknown */
export interface PositionnedEntitySpec {
  Entity: unknown;
  Orientation: unknown;
  Position: unknown;
  SpawnInModeMask: unknown;
}

/** both */
export interface PotentialLoot {
  BoostIGC: number;
  BoostLifeForce: number;
  BoostXp: number;
  IGC: number;
  IGCMineCount: number;
  LeagueBonusIGC: number;
  LeagueBonusLifeForce: number;
  LifeForce: number;
  LifeForceMineCount: number;
  MinesStealableIGC: number;
  MinesStealableLifeForce: number;
  MinesStealablePremiumCash: number;
  PremiumCashMineCount: number;
  RareDefenseIngredientRatio: number;
  TreasureRoomStealableIGC: number;
  TreasureRoomStealableLifeForce: number;
  Xp: number;
}

/** request */
export interface PotionConsumableTemplate {
  RestorePoints: number;
}

/** both */
export interface PotionUsageRestriction {
  HeroLevelMax: number;
  HeroLevelMin: number;
  MaxPotionUse: number;
}

/** both */
export interface PowerUpLevelLimitation {
  ItemLevel: number;
  MaxPowerUpLevel: number;
  MinPowerUpLevel: number;
}

/** unknown */
export interface PowerUpManaOperationSpec {
  HeroItemCategoryType: unknown;
  Value: unknown;
}

/** both */
export interface PowerUpModel {
  Description: string;
  Icon: string;
  Level: number;
  Name: string;
}

/** response */
export interface PowerUpSettings {
  PowerUps: unknown;
}

/** unknown */
export interface PowerUpSpec {
  AbilitySpecContainerId: unknown;
  BuffSpecContainerId: unknown;
  CategoryType: unknown;
  DebugName: unknown;
  LayerName: unknown;
  OasisDescription: unknown;
  OasisName: unknown;
}

/** unknown */
export interface PremiumCashBoostCommunityEvent {
  MineIncreasedPremiumCash: unknown;
}

/** request */
export interface PremiumCashBoostConsumableTemplate {
  MineIncreasedPremiumCash: number;
  BuffSpecContainerId: number;
  Duration: number;
}

/** unknown */
export interface PresetTargetDefinitionSpec {
  PresetTargetDefinitionId: unknown;
}

/** both */
export interface PreviousLeagueInfo {
  PreviousLeagueId: number;
  PreviousLeagueRank: number;
  PreviousSubLeagueId: number;
  PreviousWorldRank: number;
}

/** response */
export interface PriceReductionCondition {
  DebugName: string;
  Id: number;
  PriceReduction: number;
  Title: number;
}

/** both */
export interface PriceReductionConditionModel {
  Completed: boolean;
  CurrentPrice: unknown;
  Id: number;
  Level: number;
  PriceReduction: unknown;
}

/** both */
export interface PrimaryStatModifierRange {
  MaxValue: number;
  MinValue: number;
}

/** request */
export interface PrivateAdminMessageData {
  Body: string;
}

/** request */
export interface PrivateAdminMessageNotification {
  Message: string;
}

/** request */
export interface PrivateAdminMessagePreviewData {
  Summary: string;
}

/** request */
export interface PrivateProfileModel {
  FriendshipInvitations: FriendshipInvitation;
  FriendsLeaderboard: unknown;
  HeroIconModels: HeroIconModel;
  LatestCompletedAchievements: unknown;
  Profile: unknown;
  ProfileSummaryModel: ProfileSummaryModel;
}

/** both */
export interface ProceduralBuildingRestriction {
  CanSpawnInPve: boolean;
  MaxInstances: number;
}

/** both */
export interface ProceduralRoomBuildableSpawnInfo {
  Description: string;
  RandomSpawnPositions: unknown;
  RoomBuildableType: number;
  SpecContainerId: number;
}

/** both */
export interface ProfanityContentItem {
  Filter: Filter;
}

/** both */
export interface ProfanityFilteredCastleComment {
  Language: string;
  Value: string;
}

/** both */
export interface ProfanityFilteredDescription {
  Language: string;
  Value: string;
}

/** both */
export interface ProfanityFilteredString {
  Language: string;
  Value: string;
}

/** response */
export interface ProfanityFilteringSettings {
  ContentItemApplication: string;
  ContentItemComponent: string;
  FilterBacklistSeverity: string;
}

/** both */
export interface ProfanityProofCastleComment {
  Filtered: unknown;
  Raw: string;
}

/** both */
export interface ProfanityProofDescription {
  Filtered: unknown;
  Raw: string;
}

/** both */
export interface ProfanityProofString {
  Filtered: unknown;
  Raw: string;
}

/** request */
export interface ProfilePanelNavigationModel {
  AccountId: number;
  Tab: number;
}

/** both */
export interface ProfilePictureModel {
  AvatarId: number;
  IconUrl: string;
  LayerName: string;
}

/** both */
export interface ProfilePictureModelEventArgs {
  AvatarId: number;
  IconUrl: string;
}

/** both */
export interface ProfileSearchResult {
  MaxResult: number;
  Query: string;
  Results: unknown;
}

/** both */
export interface ProfileSearchResultModel {
  MaxResult: number;
  Query: string;
  Results: unknown;
  SpecialPackModels: SpecialPackModel;
}

/** unknown */
export interface ProfileSettings {
  MaxSearchResult: unknown;
}

/** both */
export interface ProfileSummaryChangedEventArgs {
  AccountId: number;
  AvatarId: number;
  DisplayName: string;
  SpecialPackModel: SpecialPackModel;
  TrophyScore: number;
}

/** both */
export interface ProfileSummaryModel {
  AccountId: number;
  AvatarId: number;
  CanRecruit: boolean;
  CastleLevel: number;
  DisplayName: string;
  HasPendingInvitation: boolean;
  HasPendingJoinRequest: boolean;
  IsCastleAttackable: boolean;
  IsCastleAttackableForTargetedAttack: boolean;
  LeagueId: number;
  SpecialPackModel: SpecialPackModel;
  TargetedAttackAvailableCount: number;
  TrophyScore: number;
  ValidatedAttackSource: number;
}

/** both */
export interface ProgressionLock {
  CastleLevelRequirement: number;
  CastleRenovationLevelRequirement: number;
  Comment: string;
  HeroLevelRequirement: number;
  IsDisabled: boolean;
  LockedButtons: unknown;
  LockType: number;
}

/** both */
export interface ProgressionLockUpdatedEventArgs {
  AreRequirementsMet: boolean;
  CastleLevelRequirement: number;
  CastleRenovationLevelRequirement: number;
  GameButtons: unknown;
  HeroLevelRequirement: number;
  LockType: number;
}

/** unknown */
export interface ProgressionUnlocksSettings {
  PanelsHiddenAtLevel: unknown;
  PanelsShownAtLevel: unknown;
  ProgressionLocks: unknown;
}

/** both */
export interface PropertyLevelUpChance {
  Chance: number;
  LevelFrom: number;
  LevelTo: number;
  PropertyLevel: number;
}

/** both */
export interface ProxyLoadLoginPage {
  LoginPageUrl: string;
}

/** both */
export interface ProxyLoggedIn {
  LoginToken: string;
  SGToken: string;
}

/** both */
export interface ProxyMaintenanceInfoModel {
  EndTime: string;
  StartTime: string;
}

/** both */
export interface ProxySetVersionLabel {
  TextID: number;
  TextParams: unknown;
}

/** both */
export interface ProxyShowMessageBox {
  ButtonTextIDs: number;
  InfoTextID: number;
  TextParams: unknown;
  TitleTextID: number;
}

/** both */
export interface ProxyUpdateProgressionBar {
  Progress: number;
  TextID: number;
  TextParams: unknown;
}

/** request */
export interface PublicProfileModel {
  GuildHeaderModel: GuildHeaderModel;
  HasPendingInvitationFromCurrentPlayer: boolean;
  HeroIconModels: HeroIconModel;
  IsFriend: boolean;
  LatestCompletedAchievements: unknown;
  Profile: unknown;
  ProfileSummaryModel: ProfileSummaryModel;
  UbisoftCompetitionId: number;
}

/** unknown */
export interface PushModifierBuffEffectSpec {
  Modifier: unknown;
}

/** unknown */
export interface PushOperationSpec {
  Duration: unknown;
  EaseOut: unknown;
  Vector: unknown;
}

/** unknown */
export interface PushableSpec {
  PushReductionPercent: unknown;
}

/** response */
export interface QualityColorTableEntry {
  DarkColor: number;
  LightColor: number;
  Quality: unknown;
}

/** request */
export interface QuitGamePanelNavigationModel {
  IsCastleShareable: boolean;
  IsCastleValidated: boolean;
  IsNUECompleted: boolean;
}

/** both */
export interface RMClientPackagesVersion {
  ClientGamePublicationLabel: string;
  RMPackageVersions: RMPackageVersion;
}

/** both */
export interface RMLauncherPatch {
  FullDownloadSize: number;
  FullInstallUrl: string;
  PatchDownloadSize: number;
  PatchInstallUrl: string;
  RMLauncherPatchFlags: number;
  VersionName: string;
}

/** both */
export interface RMPackageId {
  MachineType: number;
  PackageName: string;
  RMPackageType: number;
}

/** both */
export interface RMPackagePatch {
  FullDownloadSize: number;
  FullInstallUrl: string;
  PatchDownloadSize: number;
  PatchInstallUrl: string;
  RMPackagePatchFlags: number;
  RMPackageVersion: RMPackageVersion;
}

/** both */
export interface RMPackageVersion {
  RMPackageId: RMPackageId;
  VersionName: string;
}

/** both */
export interface RMServerPackagesVersion {
  BranchName: string;
  GamePublicationLabel: string;
  RMPackagePatches: unknown;
}

/** both */
export interface RandomCastlesResult {
  CastleInfos: CastleInfo;
  HasReachLastPage: boolean;
}

/** both */
export interface RandomCurrencyAmount {
  Amount: unknown;
  Probability: number;
}

/** unknown */
export interface RandomEffectActivatorFieldStyleSpec {
  IsActivationsCountRandomized: unknown;
  MaxActivations: unknown;
}

/** unknown */
export interface RandomOrientationSpec {
  AllowedAngle: unknown;
  OriginOrientation: unknown;
}

/** unknown */
export interface RandomSelectorBehaviorSpec {
  ChildrenProbabilities: unknown;
}

/** unknown */
export interface RandomValueSpec {
  Max: unknown;
  Min: unknown;
}

/** both */
export interface RareDefenseIngredientColorItem {
  Colour: string;
  UpperBound: number;
}

/** unknown */
export interface ReachLeagueObjective {
  LeagueId: unknown;
  SubLeagueId: unknown;
}

/** request */
export interface ReachLevelAchievement {
  Heroes: unknown;
}

/** both */
export interface ReachLevelInfo {
  HeroSpecContainerId: number;
  Level: number;
}

/** both */
export interface ReceiveCriticalDamageVoConfig {
  DamageHpThreshold: number;
  Vo: unknown;
}

/** unknown */
export interface RectangleAreaOperationSpec {
  Length: unknown;
  Orientation: unknown;
  Width: unknown;
}

/** unknown */
export interface RectangularShape2DSpec {
  Height: unknown;
  Width: unknown;
}

/** both */
export interface RegionMapCastle {
  RegionMapId: number;
  UiContainerName: string;
}

/** request */
export interface RegionMapPanelNavigationModel {
  AttackRegionsViewModel: AttackRegionsViewModel;
  CurrentRegion: number;
  PanelName: number;
  PendingRegionsChangedViewModel: PendingRegionsChangedViewModel;
}

/** both */
export interface RegionMapSettings {
  MaxCol: number;
  RegionMapCastles: RegionMapCastle;
}

/** unknown */
export interface RemoveBuffOperationSpec {
  BuffReference: unknown;
  RemoveBuffFromAllCreators: unknown;
}

/** request */
export interface RemoveCastleRoomCommand {
  RemovedBuildingsInstanceId: number;
  RemovedCreaturesSpecContainerId: number;
  RemovedDecorationsSpecContainerId: number;
  RemovedDefenseIngredientBoostsSpecContainerId: number;
  RemovedTrapsSpecContainerId: number;
}

/** unknown */
export interface RemoveCastleTriggerCommand {
  harvestCollectingStartedEvent: unknown;
}

/** request */
export interface RenovateBuildingPanelNavigationModel {
  BuildingDescriptionOasisId: number;
  BuildingNameOasisId: number;
  BuildingType: number;
  LayerName: string;
  RequiredLevel: number;
}

/** unknown */
export interface ReplaceAbilityOperationSpec {
  AbilityToReplaceId: unknown;
  NewAbility: unknown;
}

/** both */
export interface ReplayModeConfig {
  AttackId: string;
  FileName: string;
  Repeat: boolean;
  ReplayMode: number;
}

/** both */
export interface ReplaySpeedChangedEventArgs {
  CurrentReplaySpeed: number;
}

/** both */
export interface ReplayToolbarModel {
  AttackDurationInMilliseconds: number;
  AttackerDisplayName: string;
  AttackerSpecialPackModel: unknown;
  DefenderDisplayName: string;
  DefenderSpecialPackModel: unknown;
}

/** both */
export interface ReplayUpdateTimeEventArgs {
  CurrentReplayTime: number;
  ReplayLength: number;
}

/** both */
export interface RequirementConditionLock {
  RequirementName: string;
  RequirementRank: number;
}

/** unknown */
export interface RescaleAndClampValueSpec {
  Max: unknown;
  Min: unknown;
  NewMax: unknown;
  NewMin: unknown;
  Value: unknown;
}

/** both */
export interface ResearchSpec {
  ParentSpecContainerId: number;
  RequiredLevel: number;
  Tier: number;
}

/** both */
export interface ResistanceSettings {
  ResistanceReductionImmunityDuration: number;
  ResistanceRemovedMultiplier: number;
  ResistanceReplenishDuration: number;
}

/** unknown */
export interface ResistanceSpec {
  P7Z: unknown;
}

/** unknown */
export interface ResistedValueSpec {
  AddToTemporaryStunResistance: unknown;
  ResistanceType: unknown;
  Value: unknown;
}

/** request */
export interface RestartAttackPanelNavigationModel {
  CastleType: number;
  DefenderCastleName: string;
  HeroIconModel: HeroIconModel;
  HeroSpecContainerId: number;
  IsPvECompetition: boolean;
  IsTargetedAttack: boolean;
  IsTestAttack: boolean;
  TargetedAttackAvailableCount: number;
  TargetedAttackMaxCount: number;
}

/** unknown */
export interface RestartCooldownsOperationSpec {
  AbilitySpecContainers: unknown;
  AbilityTypeFlags: unknown;
  CooldownDuration: unknown;
}

/** request */
export interface RestoreMinesBuildingCommand {
  CastleBuildingIds: number;
  IsCastlePublishable: boolean;
}

/** unknown */
export interface RestrictedPositionVectorSpec {
  Position: unknown;
  RestrictionType: unknown;
}

/** both */
export interface ResurrectionCostByLevel {
  Cost: number;
  LevelFrom: number;
  LevelTo: number;
}

/** both */
export interface ResurrectionInfo {
  NextResurrectionCost: number;
  NextTrophyScoreLost: number;
  ResurrectionCost: number;
  ResurrectionCount: number;
}

/** both */
export interface Reward {
  FakeRewardItems: unknown;
  LargeIconUrl: string;
  RewardItems: unknown;
  SmallIconUrl: string;
}

/** both */
export interface RewardItemBase {
  CurrencyAmount: CurrencyAmount;
  LargeIconUrl: string;
  SmallIconUrl: string;
}

/** both */
export interface RewardItemModel {
  Count: number;
  CreatureRank: number;
  DyeInfoModel: DyeInfoModel;
  HeroItemQuality: number;
  IsCreature: boolean;
  IsHeroItem: boolean;
  ItemBase: unknown;
  LargeIconUrl: string;
  Name: string;
  SmallIconUrl: string;
  Tooltip: unknown;
}

/** both */
export interface RewardModel {
  FakeRewardItemModels: unknown;
  OverrideRewardItemModel: unknown;
  RewardItemModels: RewardItemModel;
}

/** both */
export interface RollbackUpdatedEventArgs {
  DelegatedCastleValidationPendingTime: number;
  IsDelegatedCastleValidationPending: boolean;
  IsRollbackEnabled: boolean;
  IsTestAttackButtonEnabled: boolean;
}

/** both */
export interface RoomBuildableIntersectionFlag {
  BuildableType: string;
  Flags: number;
}

/** unknown */
export interface RoomBuildableSpec {
  BuildingDuration: unknown;
  CraftingDuration: unknown;
  ExclusionShape: unknown;
  FirstSectionCellOffsetX: unknown;
  FirstSectionCellOffsetY: unknown;
  Height: unknown;
  IsAvailableInBuildMode: unknown;
  ResearchDuration: unknown;
  RoomBuildableType: unknown;
  Width: unknown;
}

/** unknown */
export interface RoomBuildingRankSpec {
  MaxRooms: unknown;
}

/** unknown */
export interface RoomChangedAssignmentTriggerSpec {
  RoomModelCategoryMask: unknown;
}

/** unknown */
export interface RoomConnectionSpec {
  Priority: unknown;
}

/** unknown */
export interface RoomConnectorNodeInfo {
  DefaultInfo: unknown;
  ZoomedInInfo: unknown;
  ZoomedOutInfo: unknown;
}

/** response */
export interface RoomConnectorNodeInfoCollection {
  RoomConnectorNodeInfos: RoomConnectorNodeInfo;
}

/** request */
export interface RoomDecorationPointsPanelNavigationModel {
  DecorationPoints: number;
  IconUrl: string;
  MaxDecorationPoints: number;
}

/** both */
export interface RoomDecorationPointsUpdatedEventArgs {
  DecorationPoints: number;
  IconUrl: string;
  MaxDecorationPoints: number;
}

/** request */
export interface RoomObject {
  AttachmentNode: number;
  Children: unknown;
  EffectName: number;
  IgnoreForRoomOrientations: number;
  Orientation: unknown;
  Probability: number;
  SpecContainerId: number;
  SpecContainerType: number;
  SpecContainerType: number;
  SpecContainerType: number;
  SpecContainerType: number;
}

/** both */
export interface RoomObstacle {
  Orientation: number;
  Thickness: number;
  Width: number;
  Width: number;
  Width: number;
}

/** both */
export interface RoomPlayerSpawnPoint {
  PlayerSpawnCellX: number;
  PlayerSpawnCellY: number;
  PlayerSpawnOrientation: unknown;
}

/** unknown */
export interface RoomProceduralBuildablesSpec {
  ProceduralRoomBuildables: unknown;
}

/** both */
export interface RoomSection {
  Passages: unknown;
  Passages: number;
  Passages: number;
}

/** unknown */
export interface RoomSpec {
  FirstSectionCellOffsetX: unknown;
  FirstSectionCellOffsetY: unknown;
  IsAvailableInBuildMode: unknown;
  MaxConstructionPoints: unknown;
  MaxDecorationPoints: unknown;
  Objects: unknown;
  PlayerSpawnCellY: unknown;
  PlayerSpawnOrientation: unknown;
  PlayerSpawnPoints: unknown;
  RoomModelCategory: unknown;
  RoomObstacles: unknown;
  RoomSections: unknown;
  RoomZones: unknown;
  SideTrapExclusionThickness: unknown;
  TrapsCapacity: unknown;
}

/** unknown */
export interface RoomSpecContainer {
  Type: unknown;
  p_O: unknown;
  SpecContainerReferenceId: unknown;
}

/** unknown */
export interface RoomSpecContainerRef {
  p_O: unknown;
  SpecContainerReferenceId: unknown;
}

/** request */
export interface RoomTooltipModel {
  DecorationSlotCount: number;
  RoomModelCategory: number;
  Type: number;
}

/** both */
export interface RoomZone {
  MaxConstructionPoints: number;
  RoomZoneCells: RoomZoneCell;
}

/** both */
export interface RoomZoneCell {
  CellTypeMask: number;
  CellTypeMask: number;
  CellTypeMask: number;
}

/** unknown */
export interface RoomZoneInfo {
  MaxConstructionPoints: unknown;
  RoomZoneId: unknown;
  Type: unknown;
}

/** response */
export interface RoomZoneInfoCollection {
  RoomZoneInfos: RoomZoneInfo;
  RoomZoneMaterialInfo: number;
}

/** unknown */
export interface RoomZoneInfoCollections {
  CollectionsDictionary: unknown;
}

/** unknown */
export interface RoomZoneMaterialInfo {
  AssetPath: unknown;
}

/** unknown */
export interface SaveOperationSpec {
  Slot: unknown;
  Vector: unknown;
}

/** unknown */
export interface SaveOrientationOperationSpec {
  Orientation: unknown;
}

/** unknown */
export interface SaveValueOperationSpec {
  Value: unknown;
}

/** unknown */
export interface SaveVectorOperationSpec {
  Vector: unknown;
}

/** unknown */
export interface SavedOrientationSpec {
  Slot: unknown;
}

/** unknown */
export interface SavedTargetSpec {
  Slot: unknown;
}

/** unknown */
export interface SavedValueSpec {
  Slot: unknown;
}

/** unknown */
export interface SavedVectorSpec {
  Slot: unknown;
}

/** unknown */
export interface ScaleVectorSpec {
  ScaleFactor: unknown;
  Value: unknown;
}

/** both */
export interface ScreenPositionModel {
  PositionX: number;
  PositionY: number;
}

/** both */
export interface ScreenResolutionModel {
  Height: number;
  Index: number;
  Text: string;
  Width: number;
}

/** both */
export interface SearchQuery {
  MaxRecord: number;
  Query: string;
}

/** unknown */
export interface SearchableSpec {
  Booleans: unknown;
}

/** request */
export interface SeasonalCompetitionModel {
  BestWorldUser: unknown;
  CurrentUser: unknown;
  Entries: unknown;
  FilterModel: FilterModel;
  IsFirstPageAvailable: boolean;
  IsNextPageAvailable: boolean;
  IsPreviousPageAvailable: boolean;
  IsRankPageAvailable: boolean;
  LeaderboardProgressBarModel: LeaderboardProgressBarModel;
  Leaders: unknown;
  NextSeasonSubLeagueModel: unknown;
  PageSize: number;
  RemainingTime: number;
  TotalCount: number;
}

/** request */
export interface SeasonalCompetitionPanelNavigationModel {
  FilterCode: string;
  IsPanelOpened: boolean;
  LeaderboardLevel: number;
  LeaderboardSeekMode: number;
}

/** both */
export interface SeasonalCompetitionRemainingTimeUpdatedEventArgs {
  RemainingTime: number;
}

/** both */
export interface SeasonalCompetitionSchedule {
  ClosingPeriod: number;
  DebugName: string;
  EntryTimeToLive: number;
  GiveRewardJobDelayMinutes: number;
  GlobalLockTimeout: number;
  ReferenceDate: string;
  SeasonalRewardConfig: SeasonalRewardConfig;
}

/** unknown */
export interface SeasonalCompetitionSettings {
  CountryAndZoneCacheValidity: unknown;
  LeaderDisplayedCount: unknown;
  Leagues: unknown;
  MaxEntriesPerRequest: unknown;
  ScheduleConfigs: unknown;
  WorldLeaderPeriodRewards: unknown;
}

/** request */
export interface SeasonalCompetitionStartedNotification {
  StartDate: string;
}

/** both */
export interface SeasonalEntitiesOverrides {
  CreaturesOverrides: unknown;
  RoomsOverrides: unknown;
  TrapsOverrides: unknown;
}

/** both */
export interface SeasonalEventInfo {
  Id: number;
  Name: string;
}

/** unknown */
export interface SeasonalOverridesSettings {
  NodeFilterGroupsToSeasonalEvents: unknown;
  SeasonalEntitiesOverridesCollection: unknown;
}

/** both */
export interface SeasonalRewardConfig {
  ClosingPeriodCount: number;
  Offset: number;
  StoredScoreCount: number;
}

/** both */
export interface SecurableObject {
  Id: string;
}

/** request */
export interface SecurableObjectPackageType {
  PackageType: number;
}

/** both */
export interface SecurityContext {
  Id: string;
}

/** request */
export interface SecurityContextBranch {
  BranchName: string;
}

/** request */
export interface SecurityContextBranchEnvironment {
  BranchName: string;
  EnvironmentName: string;
  EnvironmentType: number;
}

/** request */
export interface SecurityGroup {
  Members: unknown;
}

/** both */
export interface SecurityPermission {
  AccessType: number;
  Id: string;
  OperationType: number;
  SecurableObject: SecurableObject;
  SecurityContext: SecurityContext;
}

/** both */
export interface SecurityPrincipal {
  Name: string;
  Permissions: unknown;
}

/** both */
export interface SecurityPrincipalPermissions {
  Name: string;
  Permissions: unknown;
}

/** request */
export interface SelectHeroCommand {
  HeroId: number;
}

/** both */
export interface SelectableHeroListChangedEventArgs {
  HeroList: unknown;
}

/** unknown */
export interface SelectedBuildEntityChangedAssignmentTriggerSpec {
  GameEntityTypeMask: unknown;
}

/** unknown */
export interface SelectionBooleanSpec {
  Selections: unknown;
}

/** unknown */
export interface SelectionSpec {
  IsNot: unknown;
  SpecContainerIds: unknown;
  SpecContainerType: unknown;
}

/** unknown */
export interface SelectionsBuiltAssignmentConditionSpec {
  IgnoreIsBuilt: unknown;
  MaxCount: unknown;
  MinCount: unknown;
  Selections: unknown;
}

/** unknown */
export interface SelectionsCameraPositionSpec {
  Selections: unknown;
}

/** request */
export interface SellDefenseIngredientCommand {
  Count: number;
  ItemId: number;
  ItemType: number;
  Tier: number;
}

/** request */
export interface SellHeroItemCommand {
  BuyBackId: string;
  ClientSellPrice: unknown;
  HeroItemEntityType: number;
  SlotIndex: number;
  TemplateId: number;
}

/** unknown */
export interface SellItemObjective {
  ItemQualities: unknown;
}

/** unknown */
export interface SendEventOperationSpec {
  EventName: unknown;
}

/** unknown */
export interface SequenceEffectActivatorFieldStyleSpec {
  ActivationsMasks: unknown;
}

/** both */
export interface ServerAssignmentActionCompletedEventArgs {
  AssignmentActionIndex: number;
  AssignmentId: number;
}

/** request */
export interface ServerAssignmentActionCompletedNotification {
  AssignmentActionIndex: number;
  AssignmentId: number;
}

/** unknown */
export interface ServerAssignmentActionSpec {
  AttackRegionIds: unknown;
}

/** unknown */
export interface ServerAttackEndedAssignmentTriggerSpec {
  AttackCompletionTypeMask: unknown;
  HeroMinLevel: unknown;
}

/** request */
export interface ServerCommand {
  HeroItemSlot: number;
  InventorySlotIndex: number;
}

/** both */
export interface ServerDefinitions {
  ServerInfos: ServerInfo;
}

/** both */
export interface ServerEndAttackEndedEventArgs {
  EndAttackInfo: EndAttackInfo;
}

/** both */
export interface ServerInfo {
  ApplicationID: string;
  DeploymentServiceID: string;
  RelativePathToApplication: string;
  ServerName: string;
}

/** unknown */
export interface ServerNotificationReceivedTriggerSpec {
  NotificationType: unknown;
}

/** request */
export interface SessionTracking {
  AttackTotalTime: number;
  BuildTotalTime: number;
  IdleTime: number;
  LauncherTotalTime: number;
  LobbyTotalTime: number;
}

/** request */
export interface SetAfterAttackNavigationAssignmentActionSpec {
  GameStateType: number;
}

/** unknown */
export interface SetAttackSelectionInputEnabledAssignmentActionSpec {
  Enabled: unknown;
}

/** unknown */
export interface SetAttackSelectionLockOnAssignmentActionSpec {
  AccountId: unknown;
  LockOnDisabledPickingType: unknown;
}

/** request */
export interface SetAutoEquippableCategoryAssignmentActionSpec {
  HeroItemCategoryType: number;
  IsAutoEquip: boolean;
}

/** request */
export interface SetAvatarCommand {
  AvatarId: number;
}

/** unknown */
export interface SetBuildToolModeAssignmentActionSpec {
  BuildToolMode: unknown;
}

/** both */
export interface SetCastleInventoryItemViewedCommand {
  ItemType: number;
  SpecContainerId: number;
}

/** unknown */
export interface SetCastleRenovationLevelAssignmentActionSpec {
  CastleRenovationLevel: unknown;
}

/** unknown */
export interface SetHeroReadyLevelUpAssignmentActionSpec {
  Level: unknown;
}

/** unknown */
export interface SetImmunityOperationSpec {
  PaO: unknown;
  ImmunityTypeMask: unknown;
  ResetImmunityToDefaultValue: unknown;
}

/** request */
export interface SetLastViewedDateCommand {
  Type: number;
  ViewedDate: string;
}

/** request */
export interface SetLastViewedDefendLogCommand {
  ViewedDate: string;
}

/** request */
export interface SetLastViewedNewsCommand {
  NewsId: string;
}

/** unknown */
export interface SetLastVisitedShopCategoryAssignmentActionSpec {
  BuildingType: unknown;
  Filters: unknown;
  ShopCategory: unknown;
}

/** unknown */
export interface SetPickingBaseScaleOperationSpec {
  AffectOffset: unknown;
  Scale: unknown;
}

/** request */
export interface SetProfanityFilteringCommand {
  Enabled: boolean;
}

/** unknown */
export interface SetSelectableSpecContainersAssignmentActionSpec {
  SpecContainerIds: unknown;
  SpecContainerType: unknown;
}

/** unknown */
export interface SetShopFilterLockedAssignmentActionSpec {
  Filters: unknown;
  Lock: unknown;
}

/** unknown */
export interface Shape2DSpec {
  Booleans: unknown;
}

/** unknown */
export interface ShapeSpec {
  Pitch: unknown;
  Roll: unknown;
  Yaw: unknown;
  Height: unknown;
  Radius: unknown;
}

/** request */
export interface ShieldAddedNotification {
  ExpirableId: string;
}

/** request */
export interface ShieldEndExpirable {
  ExpirableType: number;
}

/** request */
export interface ShieldExpiredNotification {
  ExpirableId: string;
}

/** both */
export interface ShieldInfo {
  IsShielded: boolean;
  ShieldExpirableDueDate: string;
}

/** both */
export interface ShieldRemainingTimeUpdatedEventArgs {
  ShieldRemainingTime: number;
}

/** both */
export interface ShopCategoryFilter {
  DefaultValueId: number;
  Hidden: boolean;
  Type: number;
}

/** both */
export interface ShopCategoryModel {
  ShopCategory: number;
}

/** both */
export interface ShopCategorySettings {
  Category: number;
  Filters: Filter;
}

/** both */
export interface ShopConfirmationPopupModel {
  IsContainingPremiumCash: boolean;
  ShopProduct: unknown;
  Tooltip: unknown;
}

/** request */
export interface ShopConfirmationPopupPanelNavigationModel {
  BuildingId: number;
}

/** both */
export interface ShopConfirmationPopupSettings {
  OasisIdBuy: number;
  OasisIdBuyAndEquip: number;
  OasisIdTotalAfterPurchase: number;
}

/** both */
export interface ShopDiscount {
  DiscountType: number;
  ExpirationDate: string;
  PercentOff: number;
  StartDate: string;
}

/** both */
export interface ShopFilter {
  Type: number;
  Values: unknown;
}

/** both */
export interface ShopFilterModel {
  DefaultValueId: number;
  Hidden: boolean;
  SelectedValueId: number;
  Type: number;
  Values: unknown;
}

/** unknown */
export interface ShopFilterSelectedAssignmentTriggerSpec {
  ShopFilterValueId: unknown;
}

/** both */
export interface ShopFilterValue {
  Id: number;
}

/** request */
export interface ShopFilterValueDecorationCategory {
  DecorationCategoryMask: number;
  DecorationCategoryMaskName: string;
  DecorationCategoryMaskOasisId: number;
}

/** request */
export interface ShopFilterValueHero {
  HeroName: string;
  SpecContainerId: number;
  Id: number;
}

/** both */
export interface ShopFilterValueId {
  Id: number;
  Type: number;
}

/** request */
export interface ShopFilterValueLevel {
  LevelMax: number;
  LevelMin: number;
  Id: number;
}

/** request */
export interface ShopFilterValueUnifiedShop {
  FilterOasisId: number;
  FilterOasisName: string;
  ShopCategory: number;
}

/** request */
export interface ShopGlanceViewTracking {
  ItemCount: number;
  ItemId: number;
  ItemType: number;
  ShopGlanceViewInSeconds: number;
}

/** both */
export interface ShopHeroLevelBuyModel {
  ButtonText: string;
  Level: number;
  Price: unknown;
  SkuCode: string;
}

/** both */
export interface ShopItemRefreshedEventArgs {
  GetProductsViewModel: GetProductsViewModel;
}

/** both */
export interface ShopItemsListToDisplayOnlyEventArgs {
  IsDisabled: boolean;
  ShopItemIds: unknown;
}

/** both */
export interface ShopMenuNavigation {
  ShopMenuNavigationButtons: ShopMenuNavigationButton;
}

/** both */
export interface ShopMenuNavigationButton {
  EmptyMessageOasisId: number;
  GameButton: number;
  IconClass: string;
  IsDisabledInNUE: boolean;
  IsDisabledOnConsoleUI: boolean;
  IsDisabledOnPCUI: boolean;
  IsLockedDuringItemCrafting: boolean;
  IsLockedDuringItemReforging: boolean;
  IsLockedDuringItemUpgrading: boolean;
  LayerName: string;
  NewItemCount: number;
  OasisId: number;
  ShopCategoriesMerged: unknown;
  ShopCategory: number;
  ShopContext: number;
  Title: string;
  Url: string;
}

/** both */
export interface ShopNewItemsCountRefreshedEventArgs {
  ShopCategory: number;
  ShopCategoryNewItemsCount: number;
}

/** request */
export interface ShopPackOpenningModel {
  AreCraftingMaterialsAddedToBuyBack: boolean;
  MaterialCount: number;
  Materials: unknown;
}

/** request */
export interface ShopPanelNavigationModel {
  BuildingId: number;
  BuildingMaxRank: number;
  BuildingRank: number;
  BuildingType: number;
  CategoryConfigViewModel: unknown;
  EmptyMessageOasisId: number;
  ForgeMode: number;
  ForgeState: number;
  HasMetUpgradeRequirements: boolean;
  IsBuildMode: boolean;
  PrimaryShopEnabled: boolean;
  ProductsViewModel: unknown;
  ShopMenuNavigation: ShopMenuNavigation;
  Tab: number;
  Title: string;
}

/** both */
export interface ShopProductModel {
  AlreadyOwnedCount: number;
  BuildingRequirementRank: number;
  BuildingRequiremntName: string;
  BuyableCount: number;
  BuyBackCreationDate: string;
  BuyBackId: string;
  BuyButtonOasisId: number;
  BuyButtonOasisName: string;
  CanAfford: boolean;
  ConsumableType: number;
  CraftingMaterials: CraftingMaterial;
  CreatureRank: number;
  CreatureTrapCraftingItemModel: CreatureTrapCraftingItemModel;
  Description: string;
  DiscountExpirationRemainingTime: number;
  DiscountPercentOff: number;
  DiscountType: number;
  DyeInfoModel: DyeInfoModel;
  HeroLevelBuyModel: unknown;
  HeroRequirementLevel: number;
  HeroRequirementName: string;
  HidePriceAndUpgrade: boolean;
  IconUrl: string;
  InvIconUrl: string;
  IsBestSeller: boolean;
  IsBuildingRequirementMet: boolean;
  IsFullRequirementMet: boolean;
  IsHeroInFreeTrial: boolean;
  IsHeroRequirementMet: boolean;
  IsLimitedQuantity: boolean;
  IsNew: boolean;
  IsNewlyUnlocked: boolean;
  IsPremiumLocked: boolean;
  IsRare: boolean;
  IsRequirementMet: boolean;
  IsStealableMine: boolean;
  ItemCount: number;
  ItemId: number;
  ItemType: number;
  LayerName: string;
  Level: number;
  LimitedQuantityConsumed: number;
  LimitedQuantityMax: number;
  LimitedQuantityNextUnlockCastleLevelRequirement: number;
  LimitedQuantityNextUnlockQuantity: number;
  LimitedTimeInSeconds: number;
  Quality: number;
  ShopContentButtonType: number;
  ShopContext: number;
  ShowButton: boolean;
  Skus: unknown;
  SpecialPackGroup: number;
  Title: string;
  TooltipModel: TooltipModel;
  Weight: number;
}

/** both */
export interface ShopRefreshedEventArgs {
  BuildingRank: number;
  ShopPanelNavigationModel: ShopPanelNavigationModel;
}

/** response */
export interface ShopSettings {
  BuyBackTimeout: string;
  BuyButtonOasisIds: unknown;
  CategorySettings: number;
  DefaultIconFileName: string;
  Filters: number;
  InfinitePackId: number;
  NewnessDuration: string;
  SellConsumablePriceRatioIGC: number;
  SellConsumablePriceRatioPremium: number;
  SellDefenseIngredientPriceModifier: number;
  SellDefenseIngredientPricePremiumCashModifier: number;
  SellPremiumCashIGCRatio: number;
  ShopContentButtonOasisIds: unknown;
  ShopMenuNavigation: number;
  UpgradePriceModifier: number;
}

/** unknown */
export interface ShopShownAssignmentTriggerSpec {
  ShopCategory: unknown;
}

/** both */
export interface ShopSku {
  Code: string;
  CraftingMaterials: CraftingMaterial;
  CreationDate: string;
  DescriptionOasisId: number;
  Discounts: unknown;
  IconUrl: string;
  InternalDescription: string;
  IsActive: boolean;
  IsBestSeller: boolean;
  IsLimitedQuantity: boolean;
  IsLocked: boolean;
  ItemCount: number;
  ItemId: number;
  ItemType: number;
  LimitedQuantityMax: number;
  MaxOwningCount: number;
  PremiumEstimatedValue: number;
  Price: unknown;
  ShopContext: number;
  TitleOasisId: number;
  Weight: number;
}

/** unknown */
export interface ShopSkuBaseSettings {
  Skus: unknown;
  Version: unknown;
}

/** response */
export interface ShopSkuLimitedQuantityIncrease {
  Amount: number;
  SkuCode: string;
  Unlock: boolean;
}

/** both */
export interface ShopSkuModel {
  ActualPrice: unknown;
  LimitedQuantityMax: number;
  PremiumEstimatedValue: number;
  RegularPrice: unknown;
  ShopButtonUrl: string;
  SkuCode: string;
}

/** both */
export interface ShopSkuModifier {
  LimitedQuantityConsumed: number;
  LimitedQuantityMax: number;
  LimitedQuantityNextUnlockCastleLevelRequirement: number;
  LimitedQuantityNextUnlockQuantity: number;
  SkuCode: string;
  Unlock: boolean;
}

/** both */
export interface ShortcutCodeCollection {
  ControllerShortcuts: unknown;
  KeyboardShortcuts: unknown;
  MouseShortcuts: unknown;
}

/** request */
export interface ShortcutKeyCode {
  Key: number;
}

/** request */
export interface ShortcutMouseButtonCode {
  MouseButton: number;
}

/** both */
export interface ShowAttackReportEventArgs {
  AttackInfo: AttackInfo;
  HeroIconModel: HeroIconModel;
}

/** both */
export interface ShowBuildingHoverTooltipEventArgs {
  BuildingName: string;
  BuildingRank: number;
  MaxBuildingRank: number;
  SpecialMessage: string;
  SpecialMessage: number;
  SpecialMessage: number;
}

/** both */
export interface ShowCreatureHoverTooltipEventArgs {
  CameraZoom: number;
  CreatureName: string;
  IsCreatureSleeping: boolean;
  ToolTipModel: unknown;
  ToolTipModel: number;
  ToolTipModel: number;
}

/** request */
export interface ShowLotteryTicketPanelNavigationModel {
  IsOpalPanel: boolean;
  PanelName: number;
  PlayScratchAnimation: boolean;
}

/** request */
export interface ShowMoreCastleNotification {
  AttackSelectionResult: AttackSelectionResult;
  RegionId: number;
}

/** unknown */
export interface ShowOperationSpec {
  Show: unknown;
  TransitionDuration: unknown;
}

/** both */
export interface ShowPopupMenuEventArgs {
  fontSize: number;
  height: number;
  itemLabels: unknown;
  rightAligned: boolean;
  selectedItem: number;
  width: number;
  width: number;
  width: number;
}

/** unknown */
export interface ShowShopItemsOnlyAssignmentActionSpec {
  IsDisabled: unknown;
  ShopItems: unknown;
}

/** both */
export interface ShowTooltipEventArgs {
  Id: number;
  TooltipModel: TooltipModel;
  TooltipOptions: unknown;
}

/** both */
export interface ShowTrapHoverTooltipEventArgs {
  CameraZoom: number;
  IsPowered: number;
  PowerConsumption: number;
  TrapName: string;
  TrapName: number;
  TrapName: number;
}

/** both */
export interface ShowTrapPowerSupplyHoverTooltipEventArgs {
  Name: string;
  Name: number;
  Name: number;
}

/** both */
export interface ShowVictoryAnimationEventArgs {
  CastleLevel: number;
  HeroDied: boolean;
  IsCastleShielded: boolean;
  IsChestLocked: boolean;
  IsTestAttack: boolean;
  RewardModel: RewardModel;
  SleepingCreaturesCount: number;
  TimerDuration: number;
}

/** both */
export interface SimulationLaunchConfig {
  AttackRegionId: number;
  AttackSource: number;
  AttackType: number;
  CastleLoadConfig: CastleLoadConfig;
  EnvironmentSettingsType: number;
  GameStateModifier: number;
  InputMode: number;
  PlayerLoadConfig: PlayerLoadConfig;
  ReplayModeConfig: ReplayModeConfig;
  RevengeAttackId: string;
  SimulationMode: number;
  WorldName: string;
}

/** unknown */
export interface SimulationLoadedAssignmentConditionSpec {
  SimulationModeMask: unknown;
}

/** unknown */
export interface SimulationLoadedAssignmentTriggerSpec {
  SimulationModeMask: unknown;
}

/** request */
export interface SkillTreePanelNavigationModel {
  EquippedSpells: unknown;
  ExcludeModalPopupOpening: boolean;
  FamilyId: number;
  IsOpalPanel: boolean;
  SpellTrees: unknown;
}

/** unknown */
export interface SkuCommunityEvent {
  SkuCodes: unknown;
  SmartLootPriorityCrafting: unknown;
}

/** request */
export interface SkusModifiersUpdatedNotification {
  ShopSkuModifiers: ShopSkuModifier;
}

/** request */
export interface SleepyGiantAccountInformation {
  Achievements: Achievement;
}

/** both */
export interface SliderSettings {
  Max: number;
  Min: number;
  Precision: number;
  Step: number;
}

/** response */
export interface SoundEventWrapper {
  FireAndForget: boolean;
  Probability: number;
  SoundEventResource: number;
  SoundEventResourceSeasonalOverrides: unknown;
}

/** unknown */
export interface SourceValueSpec {
  Source: unknown;
  Value: unknown;
}

/** unknown */
export interface SourceVectorSpec {
  Source: unknown;
  Value: unknown;
}

/** unknown */
export interface SpawnSpec {
  Duration: unknown;
  EndOperations: unknown;
  IsInvincible: unknown;
  IsMoveable: unknown;
  IsPenetrable: unknown;
  IsPickingActive: unknown;
  IsSpawnDelayed: unknown;
  SpawnPosition: unknown;
  SpawnTrigger: unknown;
  StartOperations: unknown;
}

/** unknown */
export interface SpawnableEntitySpec {
  IsDependentToSpawner: unknown;
  IsDestroyedWithSpawner: unknown;
  IsSpawnSpecApplied: unknown;
  Level: unknown;
  LifeValue: unknown;
  Orientation: unknown;
  Position: unknown;
  SaveSpawnedEntitySlot: unknown;
  SpawnableEntitySpecContainerRefId: unknown;
  SpawningEndedOperations: unknown;
  SpawningStartedOperations: unknown;
  Specialization: unknown;
  Tier: unknown;
  TemplateId: unknown;
}

/** unknown */
export interface SpawnedTargetSpec {
  InstanceIndex: unknown;
  OnlyConsiderAliveInstances: unknown;
  SpecContainerReferenceId: unknown;
  SpecContainerType: unknown;
}

/** unknown */
export interface SpawnerSpec {
  InitialSpawnedEntities: unknown;
}

/** both */
export interface Spec {
  Tag: number;
}

/** response */
export interface SpecContainer {
  Name: string;
  Specs: number;
}

/** unknown */
export interface SpecContainersSelectionSpec {
  SpecContainerIds: unknown;
  SpecContainerType: unknown;
}

/** both */
export interface SpecialPack {
  AdditionalInventoryTabCount: number;
  AdditionalWorkerCabinCount: number;
  Amounts: unknown;
  BoostedHeroes: unknown;
  BuyExclusionList: number;
  CastleVisualGroupNames: unknown;
  CraftingMaterials: CraftingMaterial;
  Creatures: unknown;
  DebugName: string;
  Decorations: unknown;
  EarlyHeroAccess: number;
  HeroItems: HeroItem;
  IconLayerName: string;
  IconUrl: string;
  IconUrlLarge: string;
  Id: number;
  PackDescriptionOasisId: number;
  PackNameOasisId: number;
  ProductPageUrl: string;
  Rank: number;
  ShopSkus: ShopSku;
  SpecialPackGroup: number;
  Traps: unknown;
  UnlockedEmotes: number;
  UnlockedThemes: number;
}

/** unknown */
export interface SpecialPackAssignmentConditionSpec {
  SpecialPacks: unknown;
}

/** both */
export interface SpecialPackModel {
  IconLayerName: string;
  IconUrl: string;
  IconUrlLarge: string;
  SpecialPackId: number;
}

/** unknown */
export interface SpecialPackSettings {
  BuyBackTimeoutForSpecialPacks: unknown;
  InfinitePackId: unknown;
  SpecialPacks: unknown;
}

/** both */
export interface Spell {
  Level: number;
  NewlyAdded: boolean;
  SpellSpecContainerId: number;
}

/** both */
export interface SpellFamilyModel {
  IconUrl: string;
  Id: number;
  LayerName: string;
  Name: string;
  NewlyAddedCount: number;
}

/** both */
export interface SpellModel {
  CurrentLevel: number;
  IconUrl: string;
  LastUnlockedLevel: number;
  LayerName: string;
  MaxLevel: number;
  Name: string;
  NewlyAdded: boolean;
  NextLevelPrice: unknown;
  NextLevelSkuCode: string;
  SpecContainerId: number;
  UnlockHeroLevelRequirement: number;
}

/** unknown */
export interface SpellOperationSpec {
  BakedSpellInfo: unknown;
  IsResistable: unknown;
  Duration: unknown;
  Position: unknown;
}

/** both */
export interface SpellShortcutKeyModel {
  AbilitySlotIndex: number;
  ShortcutKey: string;
  ShortcutMouseButton: number;
}

/** request */
export interface SpellTooltipModel {
  Cooldown: number;
  DescriptionFormulas: unknown;
  HeroDamagePerSecond: number;
  HeroLevel: number;
  HeroNameRequirement: string;
  ManaBuilder: number;
  ManaBuilderDescription: string;
  ManaCost: number;
  ManaCostPerSecond: number;
  SpellLevel: number;
  Type: number;
}

/** both */
export interface SpellTreeViewModel {
  SpellFamily: unknown;
  Spells: Spell;
}

/** both */
export interface SpellUnlockedChangedEventArgs {
  UnlockedSpell: unknown;
}

/** request */
export interface SpellUnlockedNotification {
  Spell: Spell;
}

/** request */
export interface SpellViewedCommand {
  Spell: Spell;
}

/** unknown */
export interface SpellsCooldownModifierBuffEffectSpec {
  Modifier: unknown;
}

/** unknown */
export interface SpellsManaCostModifierBuffEffectSpec {
  Modifier: unknown;
}

/** unknown */
export interface SphereShapeSpec {
  Radius: unknown;
}

/** request */
export interface StartAssignmentCommand {
  AssignmentId: number;
}

/** both */
export interface StartAttackEventArgs {
  AttackInfoModel: AttackInfoModel;
}

/** both */
export interface StartSpeedBoost {
  AParameter: number;
  Cooldown: number;
  InitialSpeedBoostMultiplier: number;
}

/** both */
export interface StarterCastleInfoModel {
  CanBePurchased: boolean;
  CastleIconName: string;
  CastleName: string;
  Description: string;
  FakePrice: string;
  IsScrollExpanded: boolean;
  SaleId: number;
}

/** unknown */
export interface StatImmunityBonusBuffEffectSpec {
  StatType: unknown;
  UseBuffCreatorAsValueSource: unknown;
  Value: unknown;
}

/** both */
export interface StatModel {
  FromValue: number;
  ShouldDisplaySign: boolean;
  StatType: number;
  ToValue: number;
}

/** unknown */
export interface StatModifierBonusBuffEffectSpec {
  IsAdditive: unknown;
  StatType: unknown;
  UseBuffCreatorAsValueSource: unknown;
  Value: unknown;
}

/** unknown */
export interface StatModifierMultiplierBuffEffectSpec {
  IsAdditive: unknown;
  StatType: unknown;
  UseBuffCreatorAsValueSource: unknown;
  Value: unknown;
}

/** unknown */
export interface StatValueSpec {
  Base: unknown;
  Multiplier: unknown;
  StatType: unknown;
  UseMasterOwnerStat: unknown;
}

/** request */
export interface StateMachineTracking {
  States: unknown;
}

/** both */
export interface StateMachineTrackingState {
  ReasonForFailure: string;
  State: string;
  Successful: boolean;
}

/** both */
export interface StealableMine {
  CastleBuildingId: number;
  IsShielded: boolean;
  MaxStealableAmount: number;
  StealableAmount: number;
  StealableHeroItems: unknown;
}

/** unknown */
export interface StealableMineBuildingSpec {
  AttackDropRatio: unknown;
  DropLootInTestAttack: unknown;
  Levels: unknown;
}

/** both */
export interface SteamAssetContextSetting {
  ItemType: number;
  Name: unknown;
  Nested: boolean;
  UserFacing: boolean;
}

/** unknown */
export interface SteamAssetSettings {
  SteamAssetContextSettings: unknown;
  TagCategorySettings: unknown;
}

/** unknown */
export interface SteamAssetSpec {
  Marketable: unknown;
  Tradable: unknown;
}

/** both */
export interface SteamAssetTagCategorySetting {
  Id: number;
  Name: unknown;
}

/** both */
export interface SteamAssetTagSetting {
  CategoryId: number;
  Name: unknown;
}

/** unknown */
export interface SteamAssetUiSpec {
  Tags: unknown;
  UseDescription: unknown;
}

/** both */
export interface SteamIconExportConfig {
  TemplateSpecs: unknown;
}

/** both */
export interface SteamIconExportTemplateSpec {
  BottomMargin: number;
  Height: number;
  LeftMargin: number;
  RightMargin: number;
  TextureName: string;
  TopMargin: number;
  Width: number;
}

/** both */
export interface SteamResult {
  Error: string;
  ShouldRetry: number;
  Success: boolean;
}

/** request */
export interface StorageBuildingInfoDataModel {
  CurrentCapacity: number;
  MaxCapacity: number;
}

/** unknown */
export interface StorageBuildingRankSpec {
  Capacity: unknown;
}

/** unknown */
export interface StorageBuildingSpec {
  CurrencyType: unknown;
  DelayBeforeDroppingLoot: unknown;
}

/** request */
export interface StorageBuildingUpgradePopupDataModel {
  NewCapacity: number;
}

/** both */
export interface StoreReplayInfo {
  FileSize: number;
}

/** unknown */
export interface StunOperationSpec {
  CheckStunImmunity: unknown;
  Duration: unknown;
  UseTrapStunDurationReductionStat: unknown;
}

/** unknown */
export interface StunableSpec {
  BaseStunResistance: unknown;
  BigFlinchDuration: unknown;
  IgnoreTrapStuns: unknown;
  SmallFlinchDuration: unknown;
  StunRecoverImmunityDuration: unknown;
  StunResistanceMax: unknown;
  TrapStunRecoverImmunityDuration: unknown;
}

/** both */
export interface SubLeague {
  AttackBonus: number;
  BaseSeasonalReward: unknown;
  Id: number;
  LargeIconUrl: string;
  LeaderClosingPeriodRewards: unknown;
  LeaderSeasonalRewards: unknown;
  LeagueMaintainReward: unknown;
  LeagueReachedReward: unknown;
  Name: unknown;
  PrefixOasisId: number;
  ScoreFrom: number;
  ScoreTo: number;
  SmallIconUrl: string;
}

/** both */
export interface SubLeagueDetailedModel {
  RewardModel: RewardModel;
  ScoreMax: number;
  ScoreMin: number;
  SubLeagueModel: SubLeagueModel;
}

/** both */
export interface SubLeagueModel {
  AttackBonus: number;
  LargeIconUrl: string;
  Name: string;
  PrefixName: string;
  SmallIconUrl: string;
}

/** unknown */
export interface SurroundableSpec {
  SurroundRadius: unknown;
}

/** both */
export interface SwitchProfileHeroEventArgs {
  HeroProfileViewModel: HeroProfileViewModel;
}

/** both */
export interface SynergyFontSettings {
  AlternateFonts: unknown;
  DefaultSynergyFontTexture: string;
}

/** unknown */
export interface TargetDefinitionSpec {
  ConfusionTargetParams: unknown;
  TargetParams: unknown;
}

/** unknown */
export interface TargetLabelSpec {
  ForceUpdate: unknown;
  TargetLabel: unknown;
}

/** unknown */
export interface TargetNameSpec {
  Name: unknown;
}

/** unknown */
export interface TargetOrientationSpec {
  Target: unknown;
}

/** unknown */
export interface TargetParams {
  KeepLastValidTarget: unknown;
}

/** unknown */
export interface TargetPositionVectorSpec {
  Target: unknown;
}

/** unknown */
export interface TargetSearchCountValueSpec {
  TargetSearchSpec: unknown;
}

/** unknown */
export interface TargetSearchSpec {
  AllianceFilter: unknown;
  ExcludeSpawner: unknown;
  GameEntityTypeMask: unknown;
  MaxDistance: unknown;
  SearchMethod: unknown;
  Selections: unknown;
  TargetType: unknown;
  KeepLastValidTarget: unknown;
}

/** unknown */
export interface TargetSpec {
  SaveTargetSlot: unknown;
  Index: unknown;
}

/** both */
export interface TargetedAttackEventArgs {
  ShowTargetedAttackNotification: boolean;
  TargetedAttackAvailableCount: number;
}

/** request */
export interface TargetedAttackExpirable {
  ExpirableType: number;
}

/** request */
export interface TargetedAttackPanelNavigationModel {
  ShouldShowTargetedAttackNotification: boolean;
  TargetedAttackAvailableCount: number;
}

/** request */
export interface TargetedAttackReloadedNotification {
  TargetedAttackAvailableCount: number;
}

/** unknown */
export interface TeleportOperationSpec {
  AllowTeleportThroughObstacles: unknown;
  TargetPosition: unknown;
}

/** response */
export interface TextFontParams {
  FontSettings: number;
  SynergyMaterialFileName: number;
}

/** both */
export interface TextUpdatedEventArgs {
  Text: string;
}

/** request */
export interface TextValidatedEventArgs {
  IsEnterPressed: boolean;
}

/** both */
export interface Thanks {
  DoubleOThanks: unknown;
  SpecialThanks: unknown;
}

/** both */
export interface Theme {
  GroupNames: number;
  InvIconUrl: string;
  LargeIconUrl: string;
  Name: unknown;
  OasisDescriptionId: number;
  PrivateTheme: boolean;
  ShopIconUrl: string;
  StartupTheme: boolean;
  SteamAssetSpec: SteamAssetSpec;
  SteamAssetUiSpec: SteamAssetUiSpec;
  ThemeId: number;
}

/** request */
export interface ThemeRemovedNotification {
  ThemeId: number;
}

/** request */
export interface ThemeRewardItem {
  ThemeId: number;
}

/** request */
export interface ThemeSelectedNotification {
  ThemeId: number;
}

/** unknown */
export interface ThemeSettings {
  CastleThemes: unknown;
}

/** request */
export interface ThemeUnlockedNotification {
  ThemeId: number;
}

/** both */
export interface Thread {
  Messages: Message;
  Participants: unknown;
  ThreadHeader: ThreadHeader;
  ThreadId: number;
  ThreadPerspective: unknown;
}

/** both */
export interface ThreadCollectionPage {
  ItemListCountPerPage: number;
  ItemListIndex: number;
  ThreadList: unknown;
  TotalThreadCount: number;
}

/** both */
export interface ThreadHeader {
  FirstMessageSentDate: string;
  LastMessageSentDate: string;
  MessageCount: number;
  Subject: string;
  ThreadType: number;
}

/** both */
export interface ThreadParticipantPerspective {
  HasReplied: boolean;
  HasUnreadMessages: boolean;
  HasUnsubscribed: boolean;
  LastReadMessageIndex: number;
}

/** request */
export interface ThreadSummary {
  LastMessagePreview: unknown;
  PartialParticipantList: unknown;
  ThreadHeader: ThreadHeader;
  ThreadId: number;
  ThreadUserPerspective: unknown;
}

/** unknown */
export interface TiersSpec {
  CraftingBuildingRequirementSpec: unknown;
  ShopBuildingRequirementSpec: unknown;
  Tiers: unknown;
  Specializations: unknown;
  TemporarySpecializationRanks: unknown;
}

/** both */
export interface TimeBonusGrantedEventArgs {
  BonusTime: number;
}

/** both */
export interface TimeCost {
  Cost: unknown;
  TimeThreshold: number;
}

/** unknown */
export interface TimeScaleOperationSpec {
  Duration: unknown;
  TimeScale: unknown;
}

/** unknown */
export interface TimeSettings {
  MaxAcceptableDesynchro: unknown;
  TimeCostTable: unknown;
}

/** unknown */
export interface TimedBuffEffectSpec {
  Operations: unknown;
}

/** unknown */
export interface TimedOperationSpec {
  CancelConditionTypeFlags: unknown;
  CreateOperationOnTarget: unknown;
  Operation: unknown;
  Time: unknown;
}

/** both */
export interface TooltipManagerSettings {
  ContainerFilename: string;
}

/** both */
export interface TooltipModel {
  CurrencyType: number;
  DeathTime: number;
  FreeSlotsRequirement: number;
  HasItemsToCollect: boolean;
  HeroDisplayName: string;
  HeroLevel: number;
  IconUrl: string;
  IsHeroInventoryLargeEnough: boolean;
  IsStorageFull: boolean;
  Type: number;
}

/** unknown */
export interface TotemBoostSpec {
  OnEachTotemActivationDefendersOperation: unknown;
  OnEachTotemActivationOperation: unknown;
  OnFirstTotemActivationDefendersOperation: unknown;
  OnFirstTotemActivationOperation: unknown;
  SnapToTotemDistance: unknown;
}

/** unknown */
export interface TotemDefenderSpec {
  TotemPointsConsumption: unknown;
}

/** unknown */
export interface TotemSpec {
  CanDropInBossRoom: unknown;
  LeashingRadius: unknown;
  LeashingWarningDistance: unknown;
  OnEachTotemActivationDefendersOperation: unknown;
  OnEachTotemActivationOperation: unknown;
  OnFirstTotemActivationDefendersOperation: unknown;
  OnFirstTotemActivationOperation: unknown;
  RestoreTotemFullHealthOnLeashingActivated: unknown;
  TotemPointsCapacity: unknown;
  TotemZone: unknown;
}

/** request */
export interface TotemTooltipModel {
  CPCapacity: number;
  HealtPoints: number;
  Level: number;
  Type: number;
}

/** both */
export interface TraceRouteHop {
  Address: string;
  Pings: number;
}

/** request */
export interface TraceRouteTracking {
  HostName: string;
  TraceRoute: unknown;
}

/** both */
export interface TrackingBase {
  GameUrl: string;
}

/** request */
export interface TrackingCommand {
  TrackingTag: unknown;
}

/** unknown */
export interface TrapPowerSupplySpec {
  PoweringCapacity: unknown;
  PoweringZoneShape: unknown;
}

/** unknown */
export interface TrapSpawnOperationSpec {
  DistanceToSpawn: unknown;
  Level: unknown;
  NumberOfTraps: unknown;
  SpawnRestrictionType: unknown;
  Trap: unknown;
}

/** unknown */
export interface TrapSpec {
  BehaviorCategoryId: unknown;
  IsPowerNeeded: unknown;
  PowerConsumption: unknown;
  XpRewardShape: unknown;
}

/** unknown */
export interface TrapSpecContainer {
  Type: unknown;
  SpecContainerReferenceId: unknown;
}

/** unknown */
export interface TrapSpecContainerRef {
  SpecContainerReferenceId: unknown;
}

/** unknown */
export interface TrapStateSpec {
  ActionTime: unknown;
  PrepareTime: unknown;
  RecoverTime: unknown;
  Repeat: unknown;
}

/** unknown */
export interface TrapTierModifierSpec {
  AdditionalChildren: unknown;
  StatsModifier: unknown;
  Tiers: unknown;
}

/** unknown */
export interface TrapTiersSpec {
  TierModifiers: unknown;
}

/** request */
export interface TrapTooltipModel {
  IsPowerNeeded: boolean;
  PowerConsumption: number;
  PowerSupplied: number;
  ShowTotemBoostHint: boolean;
}

/** unknown */
export interface TrapsSettings {
  AutoReconnectFeedbackTime: unknown;
  GlobalTrapDamageMultiplier: unknown;
  GlobalTrapHealthMultiplier: unknown;
}

/** both */
export interface TreasureChestLockCountdown {
  CPFrom: number;
  CPTo: number;
  DurationsByVictoryCondition: unknown;
}

/** unknown */
export interface TreasureChestSpec {
  DelayBeforeDroppingLoot: unknown;
}

/** both */
export interface TreasureRoomChestLockInfo {
  Animation: number;
}

/** both */
export interface TreasureRoomGoldPileEntry {
  MaxAmount: number;
  MinAmount: number;
  PileCount: number;
}

/** both */
export interface TreasureRoomLoot {
  GoldDrops: number;
  HeroItem: HeroItem;
  LifeForceDrops: number;
  Xp: number;
}

/** unknown */
export interface TriggerEventAssignmentTriggerSpec {
  GameEntityTypeMask: unknown;
  TriggerId: unknown;
  TriggerState: unknown;
}

/** both */
export interface TrophiesModifier {
  From: number;
  To: number;
  TrophyMultiplier: number;
}

/** response */
export interface TrophiesSettings {
  NumberOfStarsTrophiesModifiers: number;
}

/** both */
export interface TrophyGainBucket {
  CastleRatio: number;
  MaxCrownGain: number;
  MinCrownGain: number;
}

/** both */
export interface TrophyScoreChange {
  TrophyScoreAttackerVariation: number;
  TrophyScoreDefenderVariation: number;
}

/** both */
export interface TrophyScoreChangedEventArgs {
  TrophyScore: number;
}

/** request */
export interface TrophyScoreChangedNotification {
  TrophyScore: number;
}

/** both */
export interface UIAttackOasisSettings {
  MineTimeBonus: number;
  TimerExpired: number;
  TimeToBeat: number;
  YourTime: number;
}

/** response */
export interface UIAttackReportSettings {
  PredefinedComments: number;
}

/** unknown */
export interface UIBuildSettings {
  ContextualActionInfos: unknown;
}

/** both */
export interface UIBuildingOasisSettings {
  UpgradePanel: unknown;
}

/** both */
export interface UIBuyButtonSkuControlModel {
  BuyBackId: string;
  GridItemModel: unknown;
  SkuCode: string;
}

/** both */
export interface UICastleInventoryOasisSettings {
  OasisPanelTitle: number;
}

/** unknown */
export interface UICastleInventorySettings {
  MenuNavigationButtons: unknown;
}

/** both */
export interface UICastleValidationOasisSettings {
  CreaturesNumber: number;
  MinesNumber: number;
}

/** both */
export interface UICommonOasisSettings {
  HeroItemCategoryTypeQualifier: unknown;
}

/** unknown */
export interface UIGlobalSettings {
  BossPictureLayerNames: unknown;
  BrandedCastleBannerLayerName: unknown;
  CastlePopupRegionBossPictureLayerNames: unknown;
  CraftingMaterialLayerNames: unknown;
  CreatureRankColorTable: unknown;
  CurrencyLayerNames: unknown;
  DefaultIconLayerName: unknown;
  DefaultIconSynergyName: unknown;
  ForgeNotificationIconLayerNames: unknown;
  HeroIcon: unknown;
  LanguageCodeLayerNames: unknown;
  LevelBackgroundBannerLayerNames: unknown;
  LevelBackgroundBigLayerNames: unknown;
  LevelBackgroundLargeLayerNames: unknown;
  LevelBackgroundMediumLayerNames: unknown;
  QualityColorTable: unknown;
  RankIconLayerNames: unknown;
  RegionBossPictureLayerNames: unknown;
  RenovationBuildingIconNames: unknown;
  ShortcutIcons: unknown;
  SkillEmptySlotLayerName: unknown;
  UbisoftCastleBannerLayerName: unknown;
  UserCastleBannerLayerName: unknown;
  XpLayerName: unknown;
}

/** both */
export interface UIGridItemModel {
  BuildingRequirementName: string;
  BuildingRequirementRank: number;
  ButtonName: string;
  BuyBackId: string;
  BuyButtonOasisName: string;
  CanAfford: boolean;
  CanDisableParentContainerInput: boolean;
  ConsumableType: number;
  CraftingMaterialModels: CraftingMaterialModel;
  CreatureRank: number;
  DiscountPercentOff: number;
  DiscountType: number;
  DyeInfoModel: DyeInfoModel;
  HeroRequirementLevel: number;
  HeroRequirementName: string;
  HideBuyButton: boolean;
  IsBuildingRequirementMet: boolean;
  IsCraftable: boolean;
  IsHeroRequirementMet: boolean;
  IsLimitedQuantityV2: boolean;
  IsLimitedTimeIconVisible: boolean;
  IsLocked: boolean;
  IsNewlyUnlocked: boolean;
  IsPremiumLocked: boolean;
  IsRankIconVisible: boolean;
  IsRare: boolean;
  IsShopPanelContext: boolean;
  IsSimpleBuyButton: boolean;
  IsStealableMine: boolean;
  ItemCount: number;
  ItemId: number;
  ItemName: string;
  ItemType: number;
  LayerName: string;
  Level: number;
  LockText: string;
  MaxAffordableCount: number;
  MaxAffordableCountV2: number;
  MaxLimitedCount: number;
  MaxLimitedCountV2: number;
  MaxOwningCountV2: number;
  OwnedCountV2: number;
  Quality: number;
  RankIconLayerName: string;
  RemainingLimitedCount: number;
  RemainingLimitedCountV2: number;
  ShopContext: number;
  Skus: unknown;
  StackCount: number;
  TooltipModel: TooltipModel;
}

/** request */
export interface UIGridSkuModel {
  ActualPrice: unknown;
  BuyableCount: number;
  IsLimitedQuantity: boolean;
  PremiumEstimatedValue: number;
  RegularPrice: unknown;
  ShopButtonUrl: string;
  SkuCode: string;
}

/** both */
export interface UIHeroDeathSettings {
  HealCost: number;
  LostCrown: number;
}

/** both */
export interface UIItemSlotModel {
  EquippedItemModel: unknown;
  InventoryItemModel: unknown;
}

/** both */
export interface UILocalizedLanguageCode {
  Code: string;
  OasisId: number;
}

/** unknown */
export interface UIOasisSettings {
  Attack: unknown;
  Building: unknown;
  CastleInventory: unknown;
  CastleValidation: unknown;
  Common: unknown;
  HeroDeath: unknown;
  Languages: unknown;
  PausePanel: unknown;
  ProfilePanelSettings: unknown;
  Shop: unknown;
  TimeFormatter: unknown;
  Tooltip: unknown;
  ValidateCastleSettings: unknown;
}

/** both */
export interface UIOptionInformation {
  Text: string;
}

/** unknown */
export interface UIPanelSettings {
  DefaultIconOffset3D: unknown;
  DefaultZoomSettings: unknown;
  PanelManagerContainerFilename: unknown;
  Panels: unknown;
  TooltipManagerSettings: unknown;
}

/** both */
export interface UIPausePanelOasisSettings {
  ButtonContinue: number;
  ButtonControls: number;
  ButtonCredits: number;
  ButtonExit: number;
  ButtonLeaveCastle: number;
  ButtonRestartCastle: number;
  ButtonSettings: number;
}

/** both */
export interface UIProfilePanelSettings {
  OasisIdAchievementScore: number;
  OasisIdCastlesLooted: number;
  OasisIdCreaturesDefeated: number;
  OasisIdCrowns: number;
  OasisIdGoldCollected: number;
  OasisIdHeroesDefeated: number;
  OasisIdTimeAttacksCreated: number;
  OasisIdTimeAttacksParticipated: number;
  OasisIdTimeAttacksWon: number;
  OasisIdWinningStreak: number;
}

/** both */
export interface UIShopOasisSettings {
  RequirementBuilding: number;
  RequirementHero: number;
}

/** request */
export interface UISkillSlotModel {
  EquippedHeroConsumableItemModel: EquippedHeroConsumableItemModel;
  EquippedSpellModel: EquippedSpellModel;
  IsPotionSlot: boolean;
  SpellModel: SpellModel;
}

/** both */
export interface UIStatParameter {
  DescriptionOasisId: number;
  FloatPrecision: number;
  IsPercentage: boolean;
  NameOasisId: number;
}

/** unknown */
export interface UIStatsSettings {
  StatsSettings: unknown;
}

/** both */
export interface UITabInventoryModel {
  TabIndex: number;
}

/** both */
export interface UITimeFormatterOasisSettings {
  AFewSecondsAgo: number;
  Day: number;
  Days: number;
  Hour: number;
  Hours: number;
  Minute: number;
  Minutes: number;
  Month: number;
  Months: number;
  Second: number;
  Seconds: number;
  Week: number;
  Weeks: number;
  XAgo: number;
  XLeft: number;
}

/** both */
export interface UITooltipOasisSettings {
  BuildingRequirement: number;
  CreatureAttackSpeed: number;
  CreatureMovementSpeed: number;
  ItemRank: number;
  LevelAbbreviation: number;
  LevelRequirement: number;
  TrapPowerCost: number;
}

/** both */
export interface UIUpgradePanelOasisSettings {
  Capacity: number;
  Health: number;
  ProductionRate: number;
  Rank: number;
}

/** both */
export interface UIValidateCaslteOasisSettings {
  BuyValidateDescriptionText: number;
  GuildValidationButtonText: number;
  GuildValidationDescriptionText: number;
  TicketButtonText: number;
  TicketDescriptionText: number;
  ValidateButtonText: number;
  ValidateDescriptionText: number;
}

/** both */
export interface UbisoftCastle {
  ActivationDate: string;
  CastleIconUrl: string;
  CastleValidationDuration: number;
  DeActivationDate: string;
  ForceCastleLevelOnBuildables: boolean;
  IsBranded: boolean;
  IsDisabled: boolean;
  IsForSaleCastle: boolean;
  IsHidden: boolean;
  IsTutorialCastle: boolean;
  Level: number;
  OasisDescription: number;
  OasisName: number;
}

/** response */
export interface UbisoftCompetitionAttackerRewardTier {
  MaxParticipantCount: number;
  MinParticipantCount: number;
  RewardsByAttackerRank: number;
}

/** request */
export interface UbisoftCompetitionDetailPanelNavigationModel {
  UbisoftCompetitionId: number;
}

/** both */
export interface UbisoftCompetitionInfo {
  BestScore: number;
  CastleId: number;
  CastleLevel: number;
  CastleName: string;
  CastleType: number;
  CurrentUserLeaderboardEntry: unknown;
  FriendLeaderboard: unknown;
  GlobalLeaderboard: unknown;
  MaxReward: unknown;
  MinParticipantRequired: number;
  OasisNameId: number;
  ParticipantCount: number;
  RemainingTime: number;
  UbisoftCompetitionId: number;
  UbisoftCompetitionWasEnded: boolean;
}

/** both */
export interface UbisoftCompetitionInfoModel {
  CurrentUserLeaderboardEntry: unknown;
  MaxHeroLevel: number;
  RemainingTime: number;
  TopUserLeaderboardEntry: unknown;
  UbisoftCompetitionId: number;
}

/** both */
export interface UbisoftCompetitionLeaderboardEntry {
  AccountSummary: AccountSummary;
  IsFriend: boolean;
  Rank: number;
  Reward: Reward;
  Score: number;
}

/** response */
export interface UbisoftCompetitionSchedule {
  Periods: number;
}

/** response */
export interface UbisoftCompetitionSchedulePeriod {
  CastleIds: number;
}

/** unknown */
export interface UbisoftCompetitionSettings {
  AttackerRewardTable: unknown;
  CheckEndedCompetitionBackwardLimit: unknown;
  CleanDuration: unknown;
  CompetitionCreationTimeout: unknown;
  CompetitionDuration: unknown;
  CompetitionReferenceDate: unknown;
  CompetitionSchedule: unknown;
  LeaderboardPageSize: unknown;
  MaxCastlesInSelection: unknown;
  MaxLeaderboardEntries: unknown;
  PermanentCompetitionCastleIds: unknown;
}

/** request */
export interface UbisoftCompetitionSummary {
  CastleId: number;
  CastleName: string;
  CastleType: number;
  Duration: number;
  HeroLevel: number;
  LastMessageSummary: string;
  LeaderLeaderboardEntry: unknown;
  OasisNameId: number;
  ParticipantCount: number;
  RemainingTime: number;
  UbisoftCompetitionId: number;
}

/** unknown */
export interface UiBuildingInfoSpec {
  DescriptionOasisId: unknown;
  InvIconUrl: unknown;
  Ranks: unknown;
  ShopIconUrl: unknown;
}

/** both */
export interface UiBuildingRank {
  InvIconUrl: string;
  LayerName: string;
  ShopIconUrl: string;
}

/** unknown */
export interface UiCreatureBoostSpec {
  AbilityLayerName: unknown;
  CreatureLayerName: unknown;
  OasisId: unknown;
}

/** both */
export interface UiCreatureTrapDescription {
  DescriptionFormulas: unknown;
  DescriptionOasisId: number;
  IconUrl: string;
  NameOasisId: number;
  Tier: number;
}

/** both */
export interface UiCreatureTrapRank {
  InvIconUrl: string;
  LayerName: string;
  ShopIconUrl: string;
}

/** both */
export interface UiCreatureTrapSpecialization {
  DebugName: string;
  Descriptions: unknown;
  SpecializationId: number;
  Unlocks: unknown;
}

/** unknown */
export interface UiCreatureTrapTiersSpec {
  Ranks: unknown;
  Specializations: unknown;
}

/** both */
export interface UiCreatureTrapUnlock {
  IconUrl: string;
  OasisId: number;
  Tier: number;
}

/** both */
export interface UiDefenseIngredientAbility {
  Formulas: unknown;
  Name: unknown;
  OnlyForTiers: number;
  Ui: unknown;
}

/** unknown */
export interface UiDefenseIngredientSpec {
  Abilities: unknown;
  TempoararyAbilities: unknown;
}

/** unknown */
export interface UiFormulaSpec {
  TaggedSpec: unknown;
  Formula: unknown;
  FormulaParams: unknown;
}

/** unknown */
export interface UiSettings {
  CurrencySettings: unknown;
  DamageFloatingTextOverrides: unknown;
  DebounceSearchValue: unknown;
  DefaultWebBrowserSettings: unknown;
  DefenseButtonsSettings: unknown;
  DefenseHudSettings: unknown;
  DefenseIngredientStatValueUiFormula: unknown;
  EnableAttackerHealthChangeValueFloatingText: unknown;
  FloatingTextsSettings: unknown;
  GearIconsMap: unknown;
  HarvestHtmlIconMaxSize: unknown;
  HarvestHtmlIconMinSize: unknown;
  HeightOffsetDefault: unknown;
  HeroInventorySettings: unknown;
  HeroItemTextParams: unknown;
  HeroSelectionExplanationTextOasisId: unknown;
  HomePanelButtonSettingsMap: unknown;
  LastVisitedShop: unknown;
  PlayerInteractionTable: unknown;
  PrimaryShopWebBrowserSettings: unknown;
  RegionMapSettings: unknown;
  ShopConfirmationPopupSettings: unknown;
  TextScrollingCharactersPerSecond: unknown;
  TimedEffectHudThreshold: unknown;
  WelcomePageSmallWebBrowserSettings: unknown;
  WelcomePageWebBrowserSettings: unknown;
  WheelSettings: unknown;
}

/** unknown */
export interface UiSpec {
  DisableLifeChangedFloatingTexts: unknown;
  HeightOffset: unknown;
  IconSynergyName: unknown;
  InvIconUrl: unknown;
  InvLayerName: unknown;
  IsHeightOffsetRelativeToScale: unknown;
  LayerName: unknown;
  ShopIconUrl: unknown;
}

/** unknown */
export interface UnLockWidgetsAssignmentActionSpec {
  AffectAllButtons: unknown;
  Buttons: unknown;
}

/** unknown */
export interface UniversalDropSettings {
  DefenseIngredientDropSettings: unknown;
  HeroUnlockTable: unknown;
  InventoryTypeTable: unknown;
  RewardTypeTable: unknown;
  ThemesUnlockTable: unknown;
  UniversalItemDropByType: unknown;
}

/** unknown */
export interface UnlockAttackRegionAssignmentActionSpec {
  AttackRegionIds: unknown;
}

/** both */
export interface UnlockButtonEventArgs {
  Button: number;
}

/** request */
export interface UnlockCastleThemePopupPanelNavigationModel {
  CanAfford: boolean;
  CurrencyAmount: CurrencyAmount;
  InvIconUrl: string;
  SkuCode: string;
  ThemeName: string;
}

/** unknown */
export interface UnlockObjectiveAssignmentActionSpec {
  ObjectiveId: unknown;
}

/** both */
export interface UnlockedObjectivesModel {
  Objectives: Objective;
}

/** both */
export interface UnreadInformation {
  TotalUnreadThreadCount: number;
  UnreadThreadInformations: UnreadThreadInformation;
}

/** both */
export interface UnreadThreadInformation {
  ThreadId: number;
  UnreadMessageCount: number;
}

/** both */
export interface UpdateAttackReportEventArgs {
  CrownBonuses: number;
  EndAttackInfo: EndAttackInfo;
  HeroSpecContainerId: number;
  SubLeagueModel: SubLeagueModel;
  UbisoftCompetitionId: number;
}

/** both */
export interface UpdateBuildingUpgradeButtonEventArgs {
  BuildingPopupInfoViewModel: BuildingPopupInfoViewModel;
}

/** request */
export interface UpdateCastleCreatureCommand {
  AggroPropagationOffsetX: number;
  AggroPropagationOffsetZ: number;
  IsSleeping: boolean;
  TotemCastleBuildableId: number;
}

/** request */
export interface UpdateCastleTrapCommand {
  BeatIndex: number;
  PowerSupplyCastleBuildableId: number;
}

/** request */
export interface UpdateCastleTriggerCommand {
  SizeX: number;
  SizeY: number;
}

/** both */
export interface UpdatePanelScreenPositionEventArgs {
  ScreenPositionModel: ScreenPositionModel;
}

/** request */
export interface UpgradeBuildingCommand {
  BuildingUpgradeRank: number;
  ConsumedHeroInventory: unknown;
  SkuCode: string;
}

/** both */
export interface UpgradeCompletedCameraMovementSettings {
  Duration: number;
  EaseInOut: number;
  EndZoom: number;
  IgnoreFirstUpgrade: boolean;
  IgnoreNearestZoomLevel: boolean;
  TargetOnCastleCenter: boolean;
}

/** request */
export interface UpgradeItemUnlockModel {
  HasNewInstance: boolean;
  IconUrl: string;
  ItemLevel: number;
  ItemType: number;
  LayerName: string;
  SpecContainerId: number;
  Tooltip: unknown;
}

/** request */
export interface UpgradeProductionMineBuildingCommand {
  MineBuildingId: number;
  IsCastlePublishable: boolean;
}

/** both */
export interface UpgradeStatModel {
  Boost: number;
  BoostText: string;
  CurrentValue: number;
  Icon: string;
  MaxValue: number;
  NextValue: number;
  SubTitle: string;
  Title: string;
}

/** unknown */
export interface UseAbilityObjective {
  AbilityId: unknown;
}

/** unknown */
export interface UseAbilityOperationSpec {
  AbilitySlotIndex: unknown;
  UseAbilityOnChildren: unknown;
}

/** both */
export interface UserConfigurationGamePlayModel {
  AutoFireOnDirectModeEnabled: boolean;
  LootCollectorFilter: number;
  ProfanityFilterEnable: boolean;
  StopContinuousMoveOnClickReleaseEnable: boolean;
  UseCameraDamping: boolean;
}

/** request */
export interface UserConfigurationModel {
  UserConfigurationGamePlayModel: UserConfigurationGamePlayModel;
  UserConfigurationSoundModel: UserConfigurationSoundModel;
  UserConfigurationVideoModel: UserConfigurationVideoModel;
}

/** both */
export interface UserConfigurationSoundModel {
  AudioAmbienceEnable: boolean;
  AudioMasterVolumeRatio: number;
  AudioMusicEnable: boolean;
  AudioSfxEnable: boolean;
  AudioVoiceEnable: boolean;
}

/** both */
export interface UserConfigurationVideoModel {
  DefaultLevel: number;
  Distortion: boolean;
  Fog: boolean;
  FPSClamping: number;
  FPSClampingNoFocus: number;
  FXAA: number;
  Gamma: number;
  Glow: boolean;
  LensFlare: boolean;
  ObjectComplexity: number;
  PostEffects: boolean;
  RenderQuality: number;
  ScreenSize: number;
  Shadows: number;
  SSAO: number;
  UseTopFrustumOnly: boolean;
  VSync: boolean;
  WindowType: number;
}

/** response */
export interface UserInterfaceSounds {
  UiSoundsById: unknown;
}

/** request */
export interface UserMessageData {
  Body: string;
}

/** request */
export interface UserMessagePreviewData {
  Summary: string;
}

/** both */
export interface UserSettingEmote {
  AnimationName: string;
}

/** request */
export interface UserSettings {
  AttackUserSettings: AttackUserSettings;
  AudioAmbienceEnable: boolean;
  AudioMasterVolumeRatio: number;
  AudioMusicEnable: boolean;
  AudioSfxEnable: boolean;
  AudioVoiceEnable: boolean;
  AutoFireOnDirectModeEnabled: boolean;
  IsWindowMaximized: boolean;
  ProfanityFilteringEnable: boolean;
  RuntimeConfiguration: string;
  ShortcutsDictionary: unknown;
  ShortcutsDictionaryVersion: number;
  ShortcutsInstantCast: boolean;
  StopContinuousMoveOnClickRelease: boolean;
  WindowHeight: number;
  WindowWidth: number;
}

/** request */
export interface ValidationAttemptNewsData {
  AttackerDisplayName: string;
  AttackerId: number;
  AttackerSpecialPackIconUrl: string;
  RequiresUserAction: boolean;
  Type: number;
}

/** unknown */
export interface VectorNormValueSpec {
  Vector: unknown;
}

/** unknown */
export interface VectorSpec {
  SaveVectorSlot: unknown;
  Type: unknown;
}

/** both */
export interface VictoryConditionLevelChangedEventArgs {
  VictoryConditionLevel: number;
}

/** request */
export interface VictoryConditionStarAnimationPanelNavigationModel {
  PosX: number;
  PosY: number;
}

/** request */
export interface VictoryPanelNavigationModel {
  posX: number;
  posY: number;
  RewardModel: RewardModel;
}

/** both */
export interface VideoCaptureChangedEventArgs {
  Enable: boolean;
  NbFilesInFolder: number;
}

/** request */
export interface VideoCapturePanelNavigationModel {
  Capturing: boolean;
  IsOpalPanel: boolean;
  NbFilesInFolder: number;
  PanelName: number;
}

/** request */
export interface VideoCaptureTracking {
  GameStateType: number;
  IsEnable: boolean;
}

/** both */
export interface ViewFinishResizeEventArgs {
  ViewName: string;
}

/** both */
export interface ViewableItem {
  LastViewedDate: string;
  Type: number;
}

/** both */
export interface VirtualTransaction {
  AccountId: number;
  Amount: unknown;
  Description: string;
  Id: number;
  ProductId: number;
  ServerName: string;
  State: number;
  TransactionDateTime: string;
}

/** unknown */
export interface VisualAbilityLevelSpec {
  AnimActive: unknown;
  AnimPrepare: unknown;
  AnimRecover: unknown;
  RandomAnimation: unknown;
}

/** unknown */
export interface VisualAbilitySpec {
  Levels: unknown;
}

/** unknown */
export interface VisualActivateAnimationCollectionFx {
  Activate: unknown;
  StateName: unknown;
}

/** response */
export interface VisualAnimatedEntitySettings {
  AggroIdle: number;
  AggroIdleDurationAfterAbility: number;
  AggroIdleDurationDefault: number;
  BallisticKnockBack: number;
  BuilderDrag: number;
  BuilderDrop: number;
  Celebration: number;
  CelebrationLoose: number;
  ClosedDoor: number;
  CloseDoor: number;
  CreateObstacle: number;
  CriticalFlinch: number;
  DamageObstacle: number;
  Deactivated: number;
  Death: number;
  DeathAnimationMaxDuration: number;
  DefaultAbility: number;
  DefaultAttachmentBone: number;
  DefaultLeftFootBone: number;
  DefaultRightFootBone: number;
  DestroyObstacle: number;
  EmoteAnimations: number;
  Flinch: number;
  Harvest: number;
  HeroAggroIdleToIdle: number;
  HeroDiedRejoicing: number;
  HomePageAngry: number;
  HomePageVictory: number;
  HorizontalKnockBack: number;
  Idle: number;
  InteractionOpenChest: number;
  InteractionOpenDoor: number;
  InteractionsByType: unknown;
  LoopDeactivatedAnimation: boolean;
  LootAction: number;
  MineBuildingCollected: number;
  MineBuildingCollecting: number;
  MineBuildingDamageReceived: number;
  MineBuildingReadyToCollect: number;
  MineBuildingReadyToCollectIdle: number;
  Navigation: number;
  OpenDoor: number;
  OpenedDoor: number;
  Spawn: number;
  Stun: number;
  Walk: number;
}

/** unknown */
export interface VisualAnimationTagFxSpec {
  Fx: unknown;
}

/** unknown */
export interface VisualAreaFxSpec {
  AreaTriggeredFx: unknown;
}

/** unknown */
export interface VisualAsset {
  HeroSpecContainerId: unknown;
  Name: unknown;
}

/** unknown */
export interface VisualAssignmentSettings {
  VisualPopupOnTargetInfos: unknown;
}

/** unknown */
export interface VisualAttachmentStrategySpec {
  InheritParentScale: unknown;
}

/** unknown */
export interface VisualAttackSelectionSettings {
  AngleOffsetPerLevel: unknown;
  AngleVariation: unknown;
  BossCastleHeightOffset: unknown;
  BossCastleModelsByRegion: unknown;
  BossCastleRadius: unknown;
  BossCastleSpecContainerId: unknown;
  BossCastleYaw: unknown;
  CameraInitialYaw: unknown;
  CameraLocalPositionX: unknown;
  CameraLocalPositionY: unknown;
  CameraLocalPositionZ: unknown;
  CameraScrollHorizontalSensitivity: unknown;
  CameraScrollVerticalSensitivity: unknown;
  CameraVerticalFov: unknown;
  CameraZoomInertia: unknown;
  CameraZoomLocalPositionY: unknown;
  CameraZoomLocalPositionZ: unknown;
  CameraZoomStepCount: unknown;
  CameraZoomVerticalFov: unknown;
  CastleBannerOffsetX: unknown;
  CastleBannerOffsetY: unknown;
  CastleBannerOffsetZ: unknown;
  CastleBannerSizeScale: unknown;
  CastleDefeatedAnimationName: unknown;
  CastleModels: unknown;
  CastleRootNodeName: unknown;
  CastleRootNodeSynergyFilename: unknown;
  CastleScaleVariation: unknown;
  CastleSpecContainerId: unknown;
  CastleSurviveAnimationName: unknown;
  CirclesRadius: unknown;
  DebugCastleMaxHeight: unknown;
  DebugCastleMaxWidth: unknown;
  DestroyedBossCastleModelsByRegion: unknown;
  EnvironmentSynergyFilename: unknown;
  FixedRotationByThemeId: unknown;
  HeroInitialYaw: unknown;
  HorizontalSensitivity: unknown;
  InactivityTimeBeforeCameraSpan: unknown;
  MaxYawAngleBetweenCastlesInCompetitionRegion: unknown;
  MaxYawAngleBetweenCastlesInFriendRegion: unknown;
  MaxYawAngleBetweenCastlesInRegularRegions: unknown;
  NumberOfCastlePerLevel: unknown;
  OffsetBetweenFirstLevel: unknown;
  OffsetBetweenLevels: unknown;
  OffsetBetweenLevelsVariation: unknown;
  PetsScaleInfo: unknown;
  PvpCastleShownFx: unknown;
  QuestArrowAngleOffset: unknown;
  QuestArrowOffsetFromCastle: unknown;
  QuestArrowScreenBorderMarginX: unknown;
  QuestArrowScreenBorderMarginY: unknown;
  QuestCastleArrowUISynergyFileName: unknown;
  RotationInertia: unknown;
  RotationSpeedForCameraSpan: unknown;
  TowerLocalPositionY: unknown;
  TowerLocalPositionZ: unknown;
  VerticalSensitivity: unknown;
}

/** unknown */
export interface VisualAttackSettings {
  AshPileFadeoutMaterial: unknown;
  AshPileFadeoutTime: unknown;
  BoostedCreatureFxList: unknown;
  BossKilledByHeroFx: unknown;
  CelebrationFadeOutInFx: unknown;
  CelebrationLooseFx: unknown;
  CelebrationSuccessFx: unknown;
  CombativeCreatureDefendingATotemFx: unknown;
  CombativeCreatureFx: unknown;
  CreatureDeathMaterial1: unknown;
  CreatureHighlightMaterial: unknown;
  CriticalHitTriggeredByHeroFx: unknown;
  DefaultBigFlinchHitFx: unknown;
  DefaultConfusionFx: unknown;
  DefaultCriticalHitFx: unknown;
  DefaultLevelUpFx: unknown;
  DefaultMouseMovementStartFx: unknown;
  DefaultNodeHitImpactFx: unknown;
  DefaultRegenerationFx: unknown;
  DefaultSmallFlinchFx: unknown;
  DefaultStunFx: unknown;
  EliteKilledByHeroFx: unknown;
  IGCLootVariationsMaxAmountMap: unknown;
  InteractionHighlightMaterial: unknown;
  LifeForceLootVariationsMaxAmountMap: unknown;
  LifeShieldActiveFx: unknown;
  LifeShieldBreakingFx: unknown;
  LowManaPostProcessFx: unknown;
  LowManaThreshold: unknown;
  MultiKillByHeroFx: unknown;
  NavigationStartedWithBoostFx: unknown;
  NearDeathFxList: unknown;
  OldCreatureFx: unknown;
  OldCreatureMaterial: unknown;
  OldCreaturesMaterial: unknown;
  OldTrapMaterial: unknown;
  OutOfManaInvalidActionFx: unknown;
  PremiumCashLootVariationsMaxAmountMap: unknown;
  StorageChestClosedStateAnimName: unknown;
  TrapActivatedFxList: unknown;
  TrapAutoReconnectFeedbackFxList: unknown;
  TrapDeactivatedByAbilityFxList: unknown;
  TrapDeactivatedFxList: unknown;
  TrapPowerSupplyDisabledMaterial: unknown;
  TreasureRoomChestLockInfos: unknown;
}

/** unknown */
export interface VisualBeamFxSpec {
  AttachmentStrategy: unknown;
  AttachSourceOnMasterOwner: unknown;
  PlayMode: unknown;
  Scale: unknown;
  SynergyEntityFileName: unknown;
  TargetAttachmentStrategy: unknown;
}

/** unknown */
export interface VisualBoneAttachmentStrategySpec {
  AssertIfBoneMissing: unknown;
  BoneName: unknown;
  LockRotation: unknown;
}

/** unknown */
export interface VisualBuffFxSpec {
  BuffAddedFx: unknown;
  BuffReEnteredFx: unknown;
  BuffRemovedFx: unknown;
}

/** unknown */
export interface VisualBuildSettings {
  BoostCPZoneColor: unknown;
  BossInvalidBuildableMaterial: unknown;
  BossNormalBuildableMaterial: unknown;
  BossRoomOutlineMaterial: unknown;
  BossValidBuildableMaterial: unknown;
  BuiltEntityCraftingCompletedFx: unknown;
  BuiltEntityCraftingFx: unknown;
  BuiltEntityReplacedFxByBuildEntityType: unknown;
  CraftingMaterialHarvestingFx: unknown;
  CreatureAggroPropagationEditionMaterial: unknown;
  CreatureAggroPropagationMaterial: unknown;
  CreatureAggroShapeMaterial: unknown;
  DefaultAggroableFx: unknown;
  DefaultLevelUpFx: unknown;
  DefaultOverlappingRoomBuildableFx: unknown;
  DynamicCPZoneMaterial: unknown;
  ExclusionRadiusMaterial: unknown;
  FullBoostCPZoneColor: unknown;
  FullCPZoneColor: unknown;
  GoldHarvestingFx: unknown;
  GridMaterial: unknown;
  HeroCorpseHarvestingFx: unknown;
  HeroLevelUpMessage: unknown;
  InspectedBuildableMaterial: unknown;
  InspectedEntityHighlightMaterial: unknown;
  InspectedRoomOutlineMaterial: unknown;
  InvalidBuildableMaterial: unknown;
  InvalidCPZoneColor: unknown;
  InvalidEntityHiddenOverlayMaterial: unknown;
  InvalidEntityHighlightMaterial: unknown;
  InvalidEntityOffsetY: unknown;
  InvalidRoomOutlineMaterial: unknown;
  InvalidTrapRadiusColor: unknown;
  InventoryItemsHarvestingFx: unknown;
  LifeForceHarvestingFx: unknown;
  NormalBuildableMaterial: unknown;
  NormalRoomOutlineMaterial: unknown;
  NormalTrapRadiusColor: unknown;
  OutlineRoomMaterial: unknown;
  OverlappingBuildableFootprintMaterial: unknown;
  OverlappingRoomFootprintMaterial: unknown;
  PowerConnectionBeamFx: unknown;
  PowerConnectionInvalidBeamFx: unknown;
  PowerConnectionValidBeamFx: unknown;
  PoweredTrapFx: unknown;
  PremiumCashHarvestingFx: unknown;
  RoomBuildableSelectionOutlineDroppedOffsetY: unknown;
  RoomBuildableSelectionOutlinePickedUpOffsetY: unknown;
  RoomZoneMaterial: unknown;
  SelectedEntityHighlightMaterial: unknown;
  TotemConnectionInvalidBeamFx: unknown;
  TotemConnectionValidBeamFx: unknown;
  TotemLeashingDistanceReachedFx: unknown;
  TotemLeashingZoneInvalidMaterial: unknown;
  TotemLeashingZoneMaterial: unknown;
  TotemLinkBeamFx: unknown;
  TotemZoneMaterial: unknown;
  TrapDottedLength: unknown;
  TrapPowerSupplyMaterial: unknown;
  ValidBuildableMaterial: unknown;
  ValidCPZoneColor: unknown;
  ValidRoomOutlineMaterial: unknown;
  ValidTrapRadiusColor: unknown;
  VisualCurrencyIconInfos: unknown;
  VisualRoomZoneFxPerBuildableType: unknown;
  ZoomedInCameraLight: unknown;
  ZoomedInCameraLightGroundOffset: unknown;
}

/** unknown */
export interface VisualBuildableSpec {
  ApplyInertia: unknown;
  DisplayFootprint: unknown;
  DragHeight: unknown;
}

/** unknown */
export interface VisualBuildingProgressionSpec {
  OverrideConstructionPersistentFx: unknown;
  OverrideUpgradeCompletedFx: unknown;
  OverrideUpgradePersistentFx: unknown;
  PostUpgradeNotificationFx: unknown;
  UpgradeCompletedCameraMoveSettings: unknown;
  VisualProgression: unknown;
}

/** unknown */
export interface VisualCameraShakeFxSpec {
  AnimationName: unknown;
}

/** unknown */
export interface VisualCastleSettings {
  AttackSelectionCastleRankGroups: unknown;
  AttackSelectionDestroyedCastleGroups: unknown;
  BuildingConstructionPersistentFx: unknown;
  BuildingUpgradeCompletedFx: unknown;
  BuildingUpgradePersistentFx: unknown;
  CastleRankToVisualRankIndex: unknown;
  CastleRenovationVisualInfo: unknown;
  CastleVisualProgression: unknown;
  DefaultBoostedCreatureScaleIncrease: unknown;
  DefaultSleepingFx: unknown;
  DefaultStopSleepingFx: unknown;
  DirtyCastleMaxLevel: unknown;
  HomeCastleRankScaleValues: unknown;
}

/** unknown */
export interface VisualChainFxSpec {
  ChainEndedFx: unknown;
  ChainStartedFx: unknown;
  OwnerWeaponQualityChainEndedFxList: unknown;
  OwnerWeaponQualityChainStartedFxList: unknown;
}

/** unknown */
export interface VisualCharacterSpec {
  PAZ: unknown;
  HitImpactHeight: unknown;
  MoveNaturalAnimationSpeed: unknown;
  WalkAnimationHysteresisModifier: unknown;
  WalkNaturalAnimationSpeed: unknown;
  WalkSpeedThreshold: unknown;
}

/** unknown */
export interface VisualCircleShapeSpec {
  Center: unknown;
  Radius: unknown;
}

/** unknown */
export interface VisualCreatureSpecializationSpec {
  CreatureDeathMaterial: unknown;
}

/** unknown */
export interface VisualCreatureTiersSpec {
  BoostedVisual: unknown;
  IsHiddenOverlayIgnored: unknown;
  Specializations: unknown;
  TemporaryVisualRanks: unknown;
}

/** unknown */
export interface VisualDamageFxSpec {
  DamageFx: unknown;
  OwnerWeaponQualityDamageFxList: unknown;
}

/** unknown */
export interface VisualDestructibleBuildingSpec {
  ShieldedFx: unknown;
  VisualShieldedMineNodeName: unknown;
}

/** unknown */
export interface VisualDestructibleLevelSpec {
  States: unknown;
}

/** unknown */
export interface VisualDestructibleSpec {
  IsOccludable: unknown;
  Levels: unknown;
}

/** unknown */
export interface VisualDestructibleStateSpec {
  DamageThreshold: unknown;
  Name: unknown;
  StateActiveFx: unknown;
  StateEnterFx: unknown;
  StateExitFx: unknown;
  VisualNodeName: unknown;
}

/** unknown */
export interface VisualEntityFxSpec {
  EntityDestructionFxList: unknown;
  OwnerWeaponQualityPersistentFxList: unknown;
  PersistentFxList: unknown;
  PersistentLinkedToOwnerFxList: unknown;
}

/** unknown */
export interface VisualEquipmentQualityAnimationTagFxSpec {
  ItemQualityLevels: unknown;
  Slot: unknown;
}

/** unknown */
export interface VisualEventSubscriberSpec {
  AnimationName: unknown;
  EventName: unknown;
}

/** unknown */
export interface VisualFieldFxSpec {
  EntityEnterFieldFx: unknown;
  EntityLeaveFieldFx: unknown;
  FieldShowFx: unknown;
  FieldVanishFx: unknown;
  LastEntityLeaveFieldFx: unknown;
}

/** unknown */
export interface VisualFxAbilitiesLevelEquipmentOverrideSpec {
  Slot: unknown;
  TemplateId: unknown;
}

/** unknown */
export interface VisualFxAbilitiesLevelEquipmentQualitySpec {
  ItemQualityLevels: unknown;
  Slot: unknown;
}

/** unknown */
export interface VisualFxAbilitiesLevelSpec {
  Levels: unknown;
  Slot: unknown;
  TemplateId: unknown;
}

/** unknown */
export interface VisualFxAbilitiesSpec {
  ActiveFx: unknown;
  EndFx: unknown;
  InstantFx: unknown;
  PrepareFx: unknown;
  RecoverFx: unknown;
  StartFx: unknown;
}

/** unknown */
export interface VisualFxAbilitySpec {
  Fx: unknown;
  PlayUntil: unknown;
}

/** unknown */
export interface VisualFxAsset {
  PiO: unknown;
  Fx: unknown;
}

/** unknown */
export interface VisualFxSpec {
  AttachFxOn: unknown;
  ConcurentFxOnScreen: unknown;
  Disabled: unknown;
  Duration: unknown;
  ForcePlayUntilFxFinished: unknown;
  HideInModeMask: unknown;
  Name: unknown;
  StopForcedPlayFx: unknown;
  AttachmentStrategy: unknown;
  AttachSourceOnMasterOwner: unknown;
  PlayMode: unknown;
  Scale: unknown;
  SynergyEntityFileName: unknown;
  TargetAttachmentStrategy: unknown;
}

/** both */
export interface VisualFxSpecList {
  FxList: unknown;
}

/** unknown */
export interface VisualGamepadAttackSelectionSettings {
  CameraControlRotationDamping: unknown;
  CameraIdleSearchRadiusTolerance: unknown;
  CameraSnappingEnabled: unknown;
  CameraSnappingSpeedDamping: unknown;
  CameraStickSearchRadiusTolerance: unknown;
}

/** unknown */
export interface VisualGamepadAttackSettings {
  GamepadCursorSynergyFileName: unknown;
}

/** unknown */
export interface VisualGamepadBuildSettings {
  CursorSynergyFileName: unknown;
  CursorVisualNodeNames: unknown;
}

/** unknown */
export interface VisualGamepadVibrateFxSpec {
  AnimationName: unknown;
}

/** unknown */
export interface VisualGameplayEntityFxSpec {
  BigFlinch: unknown;
  CriticalHit: unknown;
  Death: unknown;
  NodeHitImpactFx: unknown;
  SmallFlinch: unknown;
  Spawn: unknown;
  StoppedEntityMovement: unknown;
}

/** unknown */
export interface VisualHandAttachmentBonesSpec {
  PBZ: unknown;
  ItemTypeBoneName: unknown;
}

/** unknown */
export interface VisualHeroFxSpec {
  PersistentCostumeIncompatibleFxList: unknown;
}

/** unknown */
export interface VisualHeroItemSettings {
  BackPartName: unknown;
  BodyPartName: unknown;
  FacePartName: unknown;
  HandsPartName: unknown;
  HeadPartName: unknown;
  ShouldersPartName: unknown;
  VisualHandAttachmentBonesSpec: unknown;
}

/** unknown */
export interface VisualHomeSettings {
  CastleSpecContainerId: unknown;
}

/** unknown */
export interface VisualInteractiveSpec {
  InteractionAnimationName: unknown;
  InteractionType: unknown;
  IsOverlayIgnored: unknown;
  OnActivatedFx: unknown;
  OnInteractionStartFx: unknown;
  OnMouseOutFx: unknown;
  OnMouseOverFx: unknown;
}

/** unknown */
export interface VisualLabelOperationFxSpec {
  Fx: unknown;
  OperationLabel: unknown;
  ReceiverType: unknown;
}

/** unknown */
export interface VisualLobbySettings {
  ActivateConsumableAnimationName: unknown;
  EntityRotationFactor: unknown;
  EquipArmorAnimationName: unknown;
  EquipWeaponAnimationName: unknown;
  HeroInventoryXREF: unknown;
  HomePagePetsScaleInfo: unknown;
  InventoryMaxFov: unknown;
  InventoryMinFov: unknown;
  InventoryPetsScaleInfo: unknown;
  PurchaseAnimationName: unknown;
  ShopItemPlaceholder: unknown;
  ShopMaxFov: unknown;
  ShopMinFov: unknown;
  ZoomFactor: unknown;
}

/** unknown */
export interface VisualLootFxSpec {
  BlinkStartedFx: unknown;
  HeroItemQualityFxs: unknown;
  PickedUpFx: unknown;
  StopFxBeforeBlinkStarted: unknown;
}

/** unknown */
export interface VisualMaterialOverlayFxSpec {
  AnimationOffset: unknown;
  CloneMaterial: unknown;
  LowSpecSynergyEntityFileName: unknown;
  NodeAttachment: unknown;
  OverrideGroupPriority: unknown;
  PriorityOffset: unknown;
  SynergyEntityFileName: unknown;
  Type: unknown;
}

/** unknown */
export interface VisualMineBuildingFxSpec {
  BoostActivatedFx: unknown;
}

/** unknown */
export interface VisualMissileFxEquipmentOverrideSpec {
  Slot: unknown;
  TemplateId: unknown;
}

/** unknown */
export interface VisualMissileFxEquipmentQualitySpec {
  ItemQualityLevels: unknown;
  Slot: unknown;
}

/** unknown */
export interface VisualMissileFxSpec {
  EntityHitFx: unknown;
  IgnoreMissileOrientationForEntityHitFx: unknown;
  IgnoreMissileOrientationForObstacleHitFx: unknown;
  MissileMovementStartedFx: unknown;
  ObstacleHitFx: unknown;
}

/** unknown */
export interface VisualMultiInstanceFxSpec {
  DelayBetweenInstance: unknown;
  Fx: unknown;
  InstanceCount: unknown;
  RandomizeDelayMax: unknown;
  RandomizeDelayMin: unknown;
  Shape: unknown;
}

/** unknown */
export interface VisualMultiStatModifierFxSpec {
  StatModifiersEffects: unknown;
}

/** unknown */
export interface VisualNodeAttachmentStrategySpec {
  FrontOffset: unknown;
  HeightOffset: unknown;
  LockRotation: unknown;
  Pitch: unknown;
  Roll: unknown;
  SideOffset: unknown;
  StickToTheWorld: unknown;
  Yaw: unknown;
}

/** unknown */
export interface VisualOperationFxSpec {
  OperationFx: unknown;
}

/** unknown */
export interface VisualOverlayOverrideSpec {
  InspectedEntityHighlightMaterial: unknown;
  InteractionHighlightMaterial: unknown;
  InvalidEntityHiddenOverlayMaterial: unknown;
  InvalidEntityHighlightMaterial: unknown;
  SelectedEntityHighlightMaterial: unknown;
}

/** unknown */
export interface VisualPartAsset {
  SynergyFileName: unknown;
}

/** unknown */
export interface VisualPickingSpec {
  OnMouseOutFx: unknown;
  OnMouseOverFx: unknown;
  OnSelectedFx: unknown;
  OnUnSelectedFx: unknown;
}

/** unknown */
export interface VisualPostProcessFxSpec {
  Priority: unknown;
  SynergyEntityFileName: unknown;
}

/** unknown */
export interface VisualRandomAnimationSettingSpec {
  AnimationName: unknown;
  MaxConsecutivePlayCount: unknown;
  Probability: unknown;
}

/** unknown */
export interface VisualRandomAnimationSpec {
  RandomIdle: unknown;
}

/** both */
export interface VisualRenderableInfo {
  TextureFileName: number;
}

/** unknown */
export interface VisualRepeatingFxSpec {
  Shape: unknown;
}

/** unknown */
export interface VisualResourceBuildingSpec {
  VisualFillingLevelParts: unknown;
}

/** unknown */
export interface VisualRoomConnectionFxSpec {
  ConnectionTypeConnectedAngle: unknown;
  ConnectionTypeConnectedFx: unknown;
  ConnectionTypeUnconnectedAngle: unknown;
  ConnectionTypeUnconnectedFx: unknown;
}

/** response */
export interface VisualRoomZoneFxCollection {
  VisualRoomZoneFx: number;
}

/** unknown */
export interface VisualScaleFxSpec {
  ScaleDuration: unknown;
  TargetScale: unknown;
}

/** unknown */
export interface VisualSpec {
  FxAttachmentScale: unknown;
  HideInModeMask: unknown;
  RotationVariance: unknown;
  Scale: unknown;
  ScaleVariance: unknown;
  SizeCategory: unknown;
  SynergyEntityFileName: unknown;
  SynergyEntityFileNameVariations: unknown;
  SynergyName: unknown;
}

/** unknown */
export interface VisualSpecialEffectNodeFxSpec {
  AttachmentStrategy: unknown;
  PlayMode: unknown;
  Scale: unknown;
  SynergyEntityFileName: unknown;
}

/** unknown */
export interface VisualSpecializationSpec {
  VisualTierResources: unknown;
  CreatureDeathMaterial: unknown;
}

/** unknown */
export interface VisualStartAnimationFxSpec {
  AnimationName: unknown;
  IsLooping: unknown;
  IsSynergyAnimation: unknown;
  UseEmoteStateToPlayAnimation: unknown;
}

/** unknown */
export interface VisualStarterCastleSelectionSettings {
  CancelCastleSelectionTransitionDuration: unknown;
  CastleModelSynergyFilenames: unknown;
  CastleSelectionTransitionDuration: unknown;
  CastleSpecContainerId: unknown;
  CastleToFloatingLandTransitionDuration: unknown;
  EnvironmentName: unknown;
  FloatingLandToHeroesTransitionDuration: unknown;
  HeroBoughtFx: unknown;
  HeroesToFloatingLandTransitionDuration: unknown;
  ZoomOnHeroesTransitionDuration: unknown;
}

/** unknown */
export interface VisualStatModifierFxSpec {
  Effects: unknown;
  StatType: unknown;
}

/** unknown */
export interface VisualStealableMineBuildingSpec {
  ShieldedFx: unknown;
  VisualShieldedMineNodeName: unknown;
}

/** unknown */
export interface VisualTierResourceSpec {
  BoostedEntityScaleIncrease: unknown;
  Scale: unknown;
  ScaleVariance: unknown;
  SynergyEntityFileName: unknown;
}

/** unknown */
export interface VisualTimeScaleFxSpec {
  TimeScale: unknown;
}

/** unknown */
export interface VisualTotemBoostFxSpec {
  BoostOverTotemFxList: unknown;
}

/** unknown */
export interface VisualTotemFxSpec {
  ParticleMaxTimeScaleModifier: unknown;
  ParticleName: unknown;
  ParticleSpeedUpDistance: unknown;
  TotemActivatedFxListByBoostId: unknown;
  TotemBoostPickedUpFxListByBoostId: unknown;
  TotemDeactivatedFxListByBoostId: unknown;
  TotemLeashingZoneFxListByBoostId: unknown;
}

/** unknown */
export interface VisualTotemSpec {
  pjO: unknown;
  VisualTotemActivatedNodeName: unknown;
  VisualTotemDeactivatedNodeName: unknown;
}

/** unknown */
export interface VisualTrailFxAttachmentStrategySpec {
  Booleans: unknown;
}

/** unknown */
export interface VisualTrailFxBoneAttachmentSpec {
  BoneName: unknown;
  OffsetX: unknown;
  OffsetY: unknown;
  OffsetZ: unknown;
  RotationX: unknown;
  RotationY: unknown;
  RotationZ: unknown;
  TrailPointOffsetOnY: unknown;
}

/** unknown */
export interface VisualTrailFxSpec {
  Attachment: unknown;
  FadeInDistance: unknown;
  FadeInTime: unknown;
  FadeOutDistance: unknown;
  FadeOutTime: unknown;
  Length: unknown;
  SegmentLifeTime: unknown;
  SpaceBetweenSegment: unknown;
  SynergyEntityFileName: unknown;
}

/** unknown */
export interface VisualTrailFxVolumeAttachmentSpec {
  Volumes: unknown;
}

/** unknown */
export interface VisualTrapFxSpec {
  TrapActivatedFxList: unknown;
  TrapDeactivatedByAbilityFxList: unknown;
  TrapDeactivatedFxList: unknown;
}

/** unknown */
export interface VisualTrapSpec {
  BoostedVisuals: unknown;
}

/** unknown */
export interface VisualVolumeAttachmentSpec {
  OffsetX: unknown;
  OffsetY: unknown;
  OffsetZ: unknown;
  VolumeName: unknown;
}

/** unknown */
export interface VisualVolumeAttachmentStrategySpec {
  LockRotation: unknown;
  VolumeName: unknown;
}

/** unknown */
export interface VisualWeaponAsset {
  SynergyFileName: unknown;
  VisualType: unknown;
}

/** response */
export interface VoiceOverSounds {
  SoundsById: unknown;
}

/** both */
export interface Wallet {
  InGameCoin: number;
  InGameCoinStorageCapacity: number;
  LifeForce: number;
  LifeForceStorageCapacity: number;
  PremiumCash: number;
}

/** request */
export interface WalletCapacityUpdatedNotification {
  Amount: number;
  CurrencyType: number;
}

/** unknown */
export interface WalletCurrencyAmountReachedAssignmentTriggerSpec {
  CurrencyAmount: unknown;
}

/** both */
export interface WalletCurrencyUpdatedEventArgs {
  AmountChangedBy: number;
  CurrencyType: number;
  IsStorageReadyToUpgrade: boolean;
  MaxAmount: number;
  NewAmount: number;
}

/** request */
export interface WalletSummaryModel {
  Gold: unknown;
  IsGoldStorageReadyToUpgrade: boolean;
  IsLifeForceStorageReadyToUpgrade: boolean;
  LifeForce: unknown;
  MaxGold: unknown;
  MaxLifeForce: unknown;
  PremiumCash: unknown;
}

/** request */
export interface WalletUpdatedNotification {
  Amounts: unknown;
  UpdateTag: number;
}

/** request */
export interface WatchedReplayTracking {
  AttackId: string;
  EndFrame: number;
  FrameCount: number;
  FrameDuration: number;
  IsValid: boolean;
  ReplayUrl: string;
}

/** request */
export interface WeaponArchetype {
  Damage: number;
  GearScoreMultiplier: number;
  HeroId: number;
  Range: number;
  Speed: number;
}

/** both */
export interface WebBrowserSettings {
  CloseButtonLeftOffset: number;
  CloseButtonTopOffset: number;
  ContentHeight: number;
  ContentWidth: number;
  EnableAudioPresets: boolean;
  FixedHeight: number;
  FixedWidth: number;
  HeightMargin: number;
  HeightRatio: number;
  HeightRatioWideScreen: number;
  HideScrollBars: boolean;
  IsFixedSize: boolean;
  Left: number;
  Name: string;
  Top: number;
  UseBlackOverlay: boolean;
  UseBorder: boolean;
  UseRatios: boolean;
  WidthMargin: number;
  WidthRatio: number;
  WidthRatioWideScreen: number;
}

/** both */
export interface WebViews {
  ErrorView: number;
  GlobalView: number;
  HtmlTo3DView: number;
  LoadingView: number;
  TopView: number;
}

/** unknown */
export interface WelcomePageSettings {
  DisplayTimeOffset: unknown;
  ForceDisplay: unknown;
}

/** both */
export interface WheelButtonSettings {
  OasisId: number;
  url: string;
}

/** request */
export interface WheelPanelNavigationModel {
  ActiveWheel: number;
  IsCastleValidated: boolean;
  LeftWheelButtonsAreDisabled: number;
  RightWheelButtonsAreDisabled: number;
}

/** both */
export interface WheelSettings {
  CastleNotValidatedLayerName: string;
  CastleValidatedLayerName: string;
  LeftWheel: unknown;
  RightWheel: unknown;
}

/** unknown */
export interface WhileInCombatBuffEffectSpec {
  Interval: unknown;
  OffCombatDelayDuration: unknown;
  Operations: unknown;
}

/** unknown */
export interface WinUbisoftCompetitionObjective {
  P5c: unknown;
}

/** request */
export interface WorkerCabinBuildingInfoDataModel {
  CurrentWorkerCount: number;
  MaxWorkerCount: number;
}

/** request */
export interface WorkerCabinBuildingUpgradePopupDataModel {
  NewWorkerCount: number;
}

/** request */
export interface WorkerCabinRewardItem {
  Count: number;
}

/** request */
export interface WorldRankReachedNewsData {
  WorldRank: number;
}

/** unknown */
export interface XPBoostCommunityEvent {
  IncreasedXp: unknown;
}

/** both */
export interface XPChangedEventArgs {
  Hero: Hero;
  LevelChanged: boolean;
  XPChanged: number;
}

/** both */
export interface XmppInfo {
  ConferenceServer: string;
  Domain: string;
  Enabled: boolean;
  Password: string;
  Port: number;
  Server: string;
  Username: string;
}

/** request */
export interface XpBoostConsumableTemplate {
  IncreasedXp: number;
}

/** request */
export interface XpLeashBoostConsumableTemplate {
  IncreasedXp: number;
  LevelDiffFrom: number;
  LevelDiffTo: number;
}

/** both */
export interface XpLootBaseCpMultiplierTableEntry {
  MaxLevel: number;
  MinLevel: number;
  XpLootBaseCpMultiplier: number;
}

/** request */
export interface XpRewardItem {
  Xp: number;
}

/** request */
export interface YoutubePanelNavigationModel {
  IsOpalPanel: boolean;
  PanelName: number;
}

/** both */
export interface Zone {
  CodeName: string;
  Name: unknown;
}

/** response */
export interface ZoneInfo {
  Data: number;
  Height: number;
  Width: number;
}

/** both */
export interface ZoneModel {
  Name: string;
  ZoneCode: string;
}

/** both */
export interface ZoomSettings {
  Distance: number;
  IsHidingTexts: boolean;
  Zoom: number;
}
