# Utils Function Catalog

Summary of top-level functions and classes within directories containing 'utils'.

## analysis\repos\agent5_repos_31_40\FocusForge\core\utils\__init__.py

## analysis\repos\agent5_repos_31_40\FocusForge\core\utils\database.py
- Classes: Database

## src\ai_automation\utils\__init__.py

## src\ai_automation\utils\filesystem.py
- Functions: make_executable

## src\core\utils\__init__.py

## src\core\utils\agent_matching.py
- Classes: AgentCapability, AgentMatchingUtils

## src\core\utils\coordination_utils.py
- Classes: CoordinationUtils

## src\core\utils\message_queue_utils.py
- Classes: MessageQueueUtils

## src\core\utils\simple_utils.py
- Functions: copy_file, create_directory, delete_file, format_string, get_file_size, get_timestamp, is_valid_path, list_files, read_file, write_file

## src\gaming\utils\__init__.py

## src\gaming\utils\gaming_alert_utils.py
- Functions: calculate_alert_priority, create_alert_id, format_alert_message, validate_alert_metadata

## src\gaming\utils\gaming_handlers.py
- Classes: GamingEventHandlers

## src\gaming\utils\gaming_monitors.py
- Classes: GamingPerformanceMonitors

## src\services\utils\__init__.py

## src\services\utils\agent_utils_registry.py
- Functions: list_agents

## src\services\utils\messaging_templates.py

## src\services\utils\onboarding_constants.py
- Functions: get_agent_assignments, get_phase_2_status, get_targets, is_phase_2_active

## src\services\utils\vector_config_utils.py
- Functions: load_simple_config

## src\services\utils\vector_integration_helpers.py
- Functions: format_search_result, generate_agent_recommendations, generate_recommendations

## src\utils\__init__.py

## src\utils\autonomous_config_orchestrator.py
- Functions: run_autonomous_config_system
- Classes: AutonomousConfigOrchestrator

## src\utils\backup.py
- Classes: BackupManager

## src\utils\config_auto_migrator.py
- Functions: auto_migrate_directory
- Classes: ConfigAutoMigrator, MigrationAction

## src\utils\config_consolidator.py
- Functions: run_configuration_consolidation
- Classes: ConfigPattern, ConfigurationConsolidator

## src\utils\config_core\__init__.py
- Functions: get_config

## src\utils\config_core\fsm_config.py
- Classes: FSMConfig

## src\utils\config_file_scanner.py
- Classes: FileScanner

## src\utils\config_models.py
- Classes: ConfigPattern

## src\utils\config_remediator.py
- Classes: ConfigRemediator, RemediationAction

## src\utils\config_scanners.py
- Classes: ConfigConstantScanner, ConfigurationScanner, EnvironmentVariableScanner, HardcodedValueScanner, SettingsPatternScanner

## src\utils\confirm.py
- Functions: confirm

## src\utils\file_operations\__init__.py

## src\utils\file_operations\backup_operations.py
- Functions: create_backup_manager
- Classes: BackupManager, BackupOperations

## src\utils\file_operations\directory_operations.py
- Classes: DirectoryOperations

## src\utils\file_operations\file_metadata.py
- Classes: FileMetadataOperations, FileOperation

## src\utils\file_operations\file_serialization.py
- Classes: DataSerializationOperations

## src\utils\file_operations\scanner_operations.py
- Classes: UnifiedFileScanner

## src\utils\file_operations\validation_operations.py
- Classes: FileValidationResult, FileValidator

## src\utils\file_scanner.py
- Classes: FileScanner

## src\utils\file_utils.py
- Classes: FileUtils

## src\utils\logger.py
- Functions: get_contract_logger, get_core_logger, get_logger, get_messaging_logger
- Classes: StructuredFormatter, V2Logger

## src\utils\logger_utils.py
- Functions: create_logger, get_logger, setup_logger

## src\utils\scanner_registry.py
- Functions: auto_register
- Classes: ScannerRegistry

## src\utils\unified_config_utils.py
- Functions: run_configuration_consolidation
- Classes: ConfigConstantScanner, ConfigPattern, ConfigurationScanner, EnvironmentVariableScanner, FileScanner, HardcodedValueScanner, SettingsPatternScanner, UnifiedConfigurationConsolidator

## src\utils\unified_file_utils.py
- Functions: create_backup_manager
- Classes: BackupManager, BackupOperations, FileValidationResult, FileValidator, UnifiedFileScanner, UnifiedFileUtils

## src\utils\unified_utilities.py
- Functions: ensure_directory, get_config_path, get_logger, get_project_root, get_unified_utility
- Classes: UnifiedUtility

## temp_repo_analysis\FocusForge\core\utils\__init__.py

## temp_repo_analysis\FocusForge\core\utils\database.py
- Classes: Database

## temp_repo_analysis\transformers\src\transformers\utils\__init__.py
- Functions: check_min_version, get_available_devices

## temp_repo_analysis\transformers\src\transformers\utils\attention_visualizer.py
- Functions: generate_attention_matrix_from_mask
- Classes: AttentionMaskVisualizer

## temp_repo_analysis\transformers\src\transformers\utils\auto_docstring.py
- Functions: _get_model_info, _get_parameter_info, _process_example_section, _process_kwargs_parameters, _process_parameter_type, _process_parameters_section, _process_regular_parameters, _process_returns_section, add_intro_docstring, auto_class_docstring, auto_docstring, auto_method_docstring, contains_type, equalize_indent, find_sig_line, format_args_docstring, get_args_doc_from_source, get_checkpoint_from_config_class, get_indent_level, get_model_name, get_placeholders_dict, parse_default, parse_docstring, parse_shape, set_min_indent
- Classes: ClassAttrs, ClassDocstring, ImageProcessorArgs, ModelArgs, ModelOutputArgs

## temp_repo_analysis\transformers\src\transformers\utils\backbone_utils.py
- Functions: _align_output_features_output_indices, get_aligned_output_features_output_indices, load_backbone, verify_backbone_config_arguments, verify_out_features_out_indices
- Classes: BackboneConfigMixin, BackboneMixin, BackboneType

## temp_repo_analysis\transformers\src\transformers\utils\bitsandbytes.py

## temp_repo_analysis\transformers\src\transformers\utils\chat_template_utils.py
- Functions: _compile_jinja_template, _convert_type_hints_to_json_schema, _get_json_schema_type, _parse_type_hint, _render_with_assistant_indices, get_json_schema, parse_google_format_docstring, render_jinja_template
- Classes: DocstringParsingException, TypeHintParsingException

## temp_repo_analysis\transformers\src\transformers\utils\constants.py

## temp_repo_analysis\transformers\src\transformers\utils\deprecation.py
- Functions: deprecate_kwarg
- Classes: Action

## temp_repo_analysis\transformers\src\transformers\utils\doc.py
- Functions: _convert_output_args_doc, _get_indent, _prepare_output_docstrings, add_code_sample_docstrings, add_end_docstrings, add_start_docstrings, add_start_docstrings_to_model_forward, copy_func, filter_outputs_from_example, get_docstring_indentation_level, replace_return_docstrings

## temp_repo_analysis\transformers\src\transformers\utils\dummy_detectron2_objects.py
- Classes: LayoutLMv2Model

## temp_repo_analysis\transformers\src\transformers\utils\dummy_essentia_and_librosa_and_pretty_midi_and_scipy_and_torch_objects.py
- Classes: Pop2PianoFeatureExtractor, Pop2PianoProcessor, Pop2PianoTokenizer

## temp_repo_analysis\transformers\src\transformers\utils\dummy_flax_objects.py
- Classes: FlaxForceTokensLogitsProcessor, FlaxForcedBOSTokenLogitsProcessor, FlaxForcedEOSTokenLogitsProcessor, FlaxGenerationMixin, FlaxLogitsProcessor, FlaxLogitsProcessorList, FlaxLogitsWarper, FlaxMinLengthLogitsProcessor, FlaxPreTrainedModel, FlaxSuppressTokensAtBeginLogitsProcessor, FlaxSuppressTokensLogitsProcessor, FlaxTemperatureLogitsWarper, FlaxTopKLogitsWarper, FlaxTopPLogitsWarper, FlaxWhisperTimeStampLogitsProcessor

## temp_repo_analysis\transformers\src\transformers\utils\dummy_mistral_common_objects.py
- Classes: MistralCommonTokenizer

## temp_repo_analysis\transformers\src\transformers\utils\dummy_music_objects.py
- Classes: Pop2PianoFeatureExtractor, Pop2PianoTokenizer

## temp_repo_analysis\transformers\src\transformers\utils\dummy_pt_objects.py
- Functions: apply_chunking_to_forward, convert_and_export_with_cache, dynamic_rope_update, get_constant_schedule, get_constant_schedule_with_warmup, get_cosine_schedule_with_warmup, get_cosine_with_hard_restarts_schedule_with_warmup, get_inverse_sqrt_schedule, get_linear_schedule_with_warmup, get_polynomial_decay_schedule_with_warmup, get_scheduler, get_wsd_schedule, model_addition_debugger_context, prune_layer, torch_distributed_zero_first
- Classes: Adafactor, AlternatingCodebooksLogitsProcessor, AttentionInterface, AttentionMaskInterface, BayesianDetectorConfig, BayesianDetectorModel, BeamScorer, BeamSearchScorer, Cache, ClassifierFreeGuidanceLogitsProcessor, ConstrainedBeamSearchScorer, Constraint, ConstraintListState, Conv1D, DisjunctiveConstraint, DynamicCache, EncoderDecoderCache, EncoderNoRepeatNGramLogitsProcessor, EncoderRepetitionPenaltyLogitsProcessor, EosTokenCriteria, EpsilonLogitsWarper, EtaLogitsWarper, ExponentialDecayLengthPenalty, ForcedBOSTokenLogitsProcessor, ForcedEOSTokenLogitsProcessor, GenerationMixin, GlueDataTrainingArguments, GlueDataset, GradientCheckpointingLayer, HQQQuantizedCache, HammingDiversityLogitsProcessor, HybridCache, InfNanRemoveLogitsProcessor, LineByLineTextDataset, LineByLineWithRefDataset, LineByLineWithSOPTextDataset, LogitNormalization, LogitsProcessor, LogitsProcessorList, MaxLengthCriteria, MaxTimeCriteria, MinLengthLogitsProcessor, MinNewTokensLengthLogitsProcessor, MinPLogitsWarper, NoBadWordsLogitsProcessor, NoRepeatNGramLogitsProcessor, OffloadedCache, OffloadedStaticCache, PhrasalConstraint, PreTrainedModel, PrefixConstrainedLogitsProcessor, QuantizedCache, QuantoQuantizedCache, RepetitionPenaltyLogitsProcessor, Seq2SeqTrainer, SequenceBiasLogitsProcessor, SinkCache, SlidingWindowCache, SquadDataTrainingArguments, SquadDataset, StaticCache, StopStringCriteria, StoppingCriteria, StoppingCriteriaList, SuppressTokensAtBeginLogitsProcessor, SuppressTokensLogitsProcessor, SynthIDTextWatermarkDetector, SynthIDTextWatermarkLogitsProcessor, SynthIDTextWatermarkingConfig, TemperatureLogitsWarper, TextDataset, TextDatasetForNextSentencePrediction, TopKLogitsWarper, TopPLogitsWarper, TorchExportableModuleWithStaticCache, Trainer, TypicalLogitsWarper, UnbatchedClassifierFreeGuidanceLogitsProcessor, WatermarkDetector, WatermarkLogitsProcessor, WhisperTimeStampLogitsProcessor

## temp_repo_analysis\transformers\src\transformers\utils\dummy_sentencepiece_and_tokenizers_objects.py
- Functions: convert_slow_tokenizer

## temp_repo_analysis\transformers\src\transformers\utils\dummy_sentencepiece_objects.py
- Classes: AlbertTokenizer, BarthezTokenizer, BartphoTokenizer, BertGenerationTokenizer, BigBirdTokenizer, CamembertTokenizer, CodeLlamaTokenizer, CpmTokenizer, DebertaV2Tokenizer, ErnieMTokenizer, FNetTokenizer, GPTSw3Tokenizer, GemmaTokenizer, LayoutXLMTokenizer, LlamaTokenizer, M2M100Tokenizer, MBart50Tokenizer, MBartTokenizer, MLukeTokenizer, MT5Tokenizer, MarianTokenizer, NllbTokenizer, PLBartTokenizer, PegasusTokenizer, ReformerTokenizer, RemBertTokenizer, SeamlessM4TTokenizer, SiglipTokenizer, Speech2TextTokenizer, SpeechT5Tokenizer, T5Tokenizer, UdopTokenizer, XGLMTokenizer, XLMProphetNetTokenizer, XLMRobertaTokenizer, XLNetTokenizer

## temp_repo_analysis\transformers\src\transformers\utils\dummy_speech_objects.py
- Classes: ASTFeatureExtractor, Speech2TextFeatureExtractor

## temp_repo_analysis\transformers\src\transformers\utils\dummy_tensorflow_text_objects.py
- Classes: TFBertTokenizer

## temp_repo_analysis\transformers\src\transformers\utils\dummy_tf_objects.py
- Functions: create_optimizer, shape_list
- Classes: AdamWeightDecay, GradientAccumulator, KerasMetricCallback, PushToHubCallback, TFForceTokensLogitsProcessor, TFForcedBOSTokenLogitsProcessor, TFForcedEOSTokenLogitsProcessor, TFGenerationMixin, TFLogitsProcessor, TFLogitsProcessorList, TFLogitsWarper, TFMinLengthLogitsProcessor, TFNoBadWordsLogitsProcessor, TFNoRepeatNGramLogitsProcessor, TFPreTrainedModel, TFRepetitionPenaltyLogitsProcessor, TFSequenceSummary, TFSharedEmbeddings, TFSuppressTokensAtBeginLogitsProcessor, TFSuppressTokensLogitsProcessor, TFTemperatureLogitsWarper, TFTopKLogitsWarper, TFTopPLogitsWarper, WarmUp

## temp_repo_analysis\transformers\src\transformers\utils\dummy_timm_and_torchvision_objects.py
- Classes: TimmWrapperImageProcessor

## temp_repo_analysis\transformers\src\transformers\utils\dummy_tokenizers_objects.py
- Classes: PreTrainedTokenizerFast

## temp_repo_analysis\transformers\src\transformers\utils\dummy_torchaudio_objects.py
- Classes: GraniteSpeechFeatureExtractor, GraniteSpeechProcessor, MusicgenMelodyFeatureExtractor, MusicgenMelodyProcessor

## temp_repo_analysis\transformers\src\transformers\utils\dummy_torchvision_objects.py
- Classes: BaseImageProcessorFast, BaseVideoProcessor

## temp_repo_analysis\transformers\src\transformers\utils\dummy_vision_objects.py
- Classes: BaseImageProcessor, ImageFeatureExtractionMixin, ImageProcessingMixin

## temp_repo_analysis\transformers\src\transformers\utils\fx.py
- Functions: _generate_random_int, _generate_supported_model_class_names, _proxies_to_metas, check_if_model_is_supported, create_cache_proxy_factory_fn, create_wrapper, gen_constructor_wrapper, get_concrete_args, is_model_supported, operator_getitem, symbolic_trace, torch_abs, torch_add, torch_arange, torch_baddbmm, torch_bmm, torch_cat, torch_einsum, torch_flip, torch_full, torch_gather, torch_index_select, torch_matmul, torch_mul, torch_nn_bcewithlogitsloss, torch_nn_conv1d, torch_nn_conv2d, torch_nn_crossentropyloss, torch_nn_embedding, torch_nn_functional_embedding, torch_nn_functional_one_hot, torch_nn_functional_relu, torch_nn_functional_scaled_dot_product_attention, torch_nn_groupnorm, torch_nn_layernorm, torch_nn_linear, torch_nn_mseloss, torch_nn_relu, torch_relu, torch_repeat_interleave, torch_roll, torch_squeeze, torch_stack, torch_tensor_baddbmm, torch_tensor_flip, torch_tensor_gather, torch_tensor_index_select, torch_tensor_mul, torch_tensor_repeat, torch_tensor_squeeze, torch_tensor_unsqueeze, torch_unique_consecutive, torch_unsqueeze, torch_where
- Classes: HFAttribute, HFCacheProxy, HFProxy, HFProxyableClassMeta, HFTracer, MetaDeviceAttribute

## temp_repo_analysis\transformers\src\transformers\utils\generic.py
- Functions: _get_frameworks_and_test_func, _is_jax, _is_mlx, _is_numpy, _is_tensorflow, _is_tf_symbolic_tensor, _is_torch, _is_torch_device, _is_torch_dtype, can_return_loss, can_return_tuple, check_model_inputs, del_attribute_from_modules, expand_dims, filter_out_non_signature_kwargs, find_labels, flatten_dict, infer_framework, infer_framework_from_repr, is_jax_tensor, is_mlx_array, is_numpy_array, is_tensor, is_tf_symbolic_tensor, is_tf_tensor, is_timm_config_dict, is_timm_local_checkpoint, is_torch_device, is_torch_dtype, is_torch_tensor, reshape, set_attribute_for_modules, squeeze, strtobool, tensor_size, to_numpy, to_py_obj, torch_float, torch_int, transpose, working_or_temp_dir
- Classes: ContextManagers, ExplicitEnum, GeneralInterface, ModelOutput, OutputRecorder, PaddingStrategy, TensorType, TransformersKwargs, cached_property

## temp_repo_analysis\transformers\src\transformers\utils\hp_naming.py
- Classes: TrialShortNamer

## temp_repo_analysis\transformers\src\transformers\utils\hub.py
- Functions: _get_cache_file_to_return, cached_file, cached_files, convert_file_size_to_int, create_and_tag_model_card, define_sagemaker_information, download_url, extract_commit_hash, get_checkpoint_shard_files, has_file, http_user_agent, is_offline_mode, is_remote_url, list_repo_templates, send_example_telemetry
- Classes: PushInProgress, PushToHubMixin

## temp_repo_analysis\transformers\src\transformers\utils\import_utils.py
- Functions: _is_package_available, check_torch_load_is_safe, clear_import_cache, create_import_structure_from_path, define_import_structure, direct_transformers_import, fetch__all__, get_sudachi_version, get_torch_major_and_minor_version, get_torch_version, is_accelerate_available, is_apex_available, is_apollo_torch_available, is_aqlm_available, is_auto_awq_available, is_auto_gptq_available, is_auto_round_available, is_av_available, is_bitsandbytes_available, is_bitsandbytes_multi_backend_available, is_bs4_available, is_causal_conv1d_available, is_ccl_available, is_coloredlogs_available, is_compressed_tensors_available, is_cuda_platform, is_cv2_available, is_cython_available, is_datasets_available, is_decord_available, is_detectron2_available, is_eetq_available, is_essentia_available, is_faiss_available, is_fastapi_available, is_fbgemm_gpu_available, is_flash_attn_2_available, is_flash_attn_3_available, is_flash_attn_greater_or_equal, is_flash_attn_greater_or_equal_2_10, is_flax_available, is_flute_available, is_fp_quant_available, is_fsdp_available, is_ftfy_available, is_g2p_en_available, is_galore_torch_available, is_gguf_available, is_gptqmodel_available, is_grokadamw_available, is_habana_gaudi1, is_hadamard_available, is_hqq_available, is_huggingface_hub_greater_or_equal, is_in_notebook, is_ipex_available, is_jieba_available, is_jinja_available, is_jumanpp_available, is_kenlm_available, is_keras_nlp_available, is_kernels_available, is_levenshtein_available, is_libcst_available, is_librosa_available, is_liger_kernel_available, is_lomo_available, is_mamba_2_ssm_available, is_mamba_ssm_available, is_mambapy_available, is_matplotlib_available, is_mistral_common_available, is_mlx_available, is_natten_available, is_ninja_available, is_nltk_available, is_num2words_available, is_onnx_available, is_openai_available, is_optimum_available, is_optimum_neuron_available, is_optimum_quanto_available, is_pandas_available, is_peft_available, is_phonemizer_available, is_pretty_midi_available, is_protobuf_available, is_psutil_available, is_py3nvml_available, is_pyctcdecode_available, is_pydantic_available, is_pygments_available, is_pytesseract_available, is_pytest_available, is_pytorch_quantization_available, is_quanto_greater, is_quark_available, is_qutlass_available, is_rich_available, is_rjieba_available, is_rocm_platform, is_sacremoses_available, is_safetensors_available, is_sagemaker_dp_enabled, is_sagemaker_mp_enabled, is_schedulefree_available, is_scipy_available, is_sentencepiece_available, is_seqio_available, is_sklearn_available, is_soundfile_available, is_spacy_available, is_speech_available, is_spqr_available, is_sudachi_available, is_sudachi_projection_available, is_tensorflow_probability_available, is_tensorflow_text_available, is_tf2onnx_available, is_tf_available, is_tiktoken_available, is_timm_available, is_tokenizers_available, is_torch_accelerator_available, is_torch_available, is_torch_bf16_available, is_torch_bf16_available_on_device, is_torch_bf16_cpu_available, is_torch_bf16_gpu_available, is_torch_compile_available, is_torch_cuda_available, is_torch_deterministic, is_torch_flex_attn_available, is_torch_fp16_available_on_device, is_torch_fx_available, is_torch_fx_proxy, is_torch_greater_or_equal, is_torch_hpu_available, is_torch_less_or_equal, is_torch_mlu_available, is_torch_mps_available, is_torch_musa_available, is_torch_neuroncore_available, is_torch_npu_available, is_torch_optimi_available, is_torch_sdpa_available, is_torch_tensorrt_fx_available, is_torch_tf32_available, is_torch_xla_available, is_torch_xpu_available, is_torchao_available, is_torchaudio_available, is_torchcodec_available, is_torchdistx_available, is_torchdynamo_available, is_torchdynamo_compiling, is_torchdynamo_exporting, is_torchvision_available, is_torchvision_v2_available, is_training_run_on_sagemaker, is_triton_available, is_uroman_available, is_uvicorn_available, is_vision_available, is_vptq_available, is_xlstm_available, is_yt_dlp_available, requires, requires_backends, split_package_version, spread_import_structure, torch_only_method
- Classes: Backend, DummyObject, OptionalDependencyNotAvailable, VersionComparison, _LazyModule

## temp_repo_analysis\transformers\src\transformers\utils\logging.py
- Functions: _configure_library_root_logger, _get_default_logging_level, _get_library_name, _get_library_root_logger, _reset_library_root_logger, add_handler, captureWarnings, disable_default_handler, disable_progress_bar, disable_propagation, enable_default_handler, enable_explicit_format, enable_progress_bar, enable_propagation, get_log_levels_dict, get_logger, get_verbosity, info_once, is_progress_bar_enabled, remove_handler, reset_format, set_verbosity, set_verbosity_debug, set_verbosity_error, set_verbosity_info, set_verbosity_warning, warning_advice, warning_once
- Classes: EmptyTqdm, _tqdm_cls

## temp_repo_analysis\transformers\src\transformers\utils\metrics.py
- Functions: attach_tracer, traced
- Classes: ContinuousBatchProcessorMetrics, RequestStatus

## temp_repo_analysis\transformers\src\transformers\utils\model_parallel_utils.py
- Functions: assert_device_map, get_device_map

## temp_repo_analysis\transformers\src\transformers\utils\notebook.py
- Functions: format_time, html_progress_bar, text_to_html_table
- Classes: NotebookProgressBar, NotebookProgressCallback, NotebookTrainingTracker

## temp_repo_analysis\transformers\src\transformers\utils\peft_utils.py
- Functions: check_peft_version, find_adapter_config_file

## temp_repo_analysis\transformers\src\transformers\utils\quantization_config.py
- Classes: AWQLinearVersion, AqlmConfig, AutoRoundConfig, AwqBackendPackingMethod, AwqConfig, BitNetQuantConfig, BitsAndBytesConfig, CompressedTensorsConfig, EetqConfig, ExllamaVersion, FPQuantConfig, FbgemmFp8Config, FineGrainedFP8Config, GPTQConfig, HiggsConfig, HqqConfig, Mxfp4Config, QuantizationConfigMixin, QuantizationMethod, QuantoConfig, QuarkConfig, SpQRConfig, TorchAoConfig, VptqConfig, VptqLayerConfig

## temp_repo_analysis\transformers\src\transformers\utils\sentencepiece_model_pb2.py

## temp_repo_analysis\transformers\src\transformers\utils\sentencepiece_model_pb2_new.py

## temp_repo_analysis\transformers\src\transformers\utils\versions.py
- Functions: _compare_versions, require_version, require_version_core

## temp_repo_analysis\transformers\tests\utils\__init__.py

## temp_repo_analysis\transformers\tests\utils\import_structures\failing_export.py
- Classes: A0

## temp_repo_analysis\transformers\tests\utils\import_structures\import_structure_raw_register.py
- Functions: a0, a1, a2, a3
- Classes: A0, A1, A2, A3, A4

## temp_repo_analysis\transformers\tests\utils\import_structures\import_structure_raw_register_with_versions.py
- Functions: d0, d1, d2, d3, d4, d5, d6
- Classes: D0, D1, D2, D3, D4, D5, D6

## temp_repo_analysis\transformers\tests\utils\import_structures\import_structure_register_with_comments.py
- Functions: b0, b1, b2, b3
- Classes: B0, B1, B2, B3

## temp_repo_analysis\transformers\tests\utils\import_structures\import_structure_register_with_duplicates.py
- Functions: c0, c1, c2, c3
- Classes: C0, C1, C2, C3

## temp_repo_analysis\transformers\tests\utils\test_activations.py
- Classes: TestActivations

## temp_repo_analysis\transformers\tests\utils\test_add_new_model_like.py
- Classes: TestAddNewModelLike

## temp_repo_analysis\transformers\tests\utils\test_attention_visualizer.py
- Functions: _normalize
- Classes: AttentionMaskVisualizerTester

## temp_repo_analysis\transformers\tests\utils\test_audio_utils.py
- Classes: AudioUtilsFunctionTester

## temp_repo_analysis\transformers\tests\utils\test_auto_docstring.py
- Classes: AutoDocstringTest

## temp_repo_analysis\transformers\tests\utils\test_backbone_utils.py
- Classes: BackboneUtilsTester

## temp_repo_analysis\transformers\tests\utils\test_cache_utils.py
- Functions: _skip_on_failed_cache_prerequisites
- Classes: CacheExportIntegrationTest, CacheHardIntegrationTest, CacheIntegrationTest, CacheTest, SyntheticCacheTest

## temp_repo_analysis\transformers\tests\utils\test_chat_template_utils.py
- Classes: JsonSchemaGeneratorTest

## temp_repo_analysis\transformers\tests\utils\test_cli.py
- Classes: CLITest

## temp_repo_analysis\transformers\tests\utils\test_configuration_utils.py
- Classes: ConfigPushToHubTester, ConfigTestUtils

## temp_repo_analysis\transformers\tests\utils\test_convert_slow_tokenizer.py
- Classes: ConvertSlowTokenizerTest, FakeOriginalTokenizer

## temp_repo_analysis\transformers\tests\utils\test_deprecation.py
- Classes: DeprecationDecoratorTester

## temp_repo_analysis\transformers\tests\utils\test_doc_samples.py
- Classes: TestCodeExamples

## temp_repo_analysis\transformers\tests\utils\test_dynamic_module_utils.py
- Functions: test_import_parsing

## temp_repo_analysis\transformers\tests\utils\test_expectations.py
- Classes: ExpectationsTest

## temp_repo_analysis\transformers\tests\utils\test_feature_extraction_utils.py
- Classes: FeatureExtractorPushToHubTester, FeatureExtractorUtilTester

## temp_repo_analysis\transformers\tests\utils\test_file_utils.py
- Functions: context_en, context_fr
- Classes: GenericUtilTests, TestImportMechanisms

## temp_repo_analysis\transformers\tests\utils\test_generic.py
- Classes: CanReturnTupleDecoratorTester, GenericTester, ValidationDecoratorTester

## temp_repo_analysis\transformers\tests\utils\test_hf_argparser.py
- Functions: list_field
- Classes: BasicEnum, BasicExample, EnumExample, HfArgumentParserTest, ListExample, MixedTypeEnum, MixedTypeEnumExample, OptionalExample, RequiredExample, StringLiteralAnnotationExample, WithDefaultBoolExample, WithDefaultExample

## temp_repo_analysis\transformers\tests\utils\test_hub_utils.py
- Classes: GetFromCacheTests

## temp_repo_analysis\transformers\tests\utils\test_image_processing_utils.py
- Classes: ImageProcessingUtilsTester, ImageProcessorPushToHubTester, ImageProcessorUtilTester

## temp_repo_analysis\transformers\tests\utils\test_image_utils.py
- Functions: get_image_from_hub_dataset, get_random_image
- Classes: ImageFeatureExtractionTester, LoadImageTester, UtilFunctionTester

## temp_repo_analysis\transformers\tests\utils\test_import_structure.py
- Functions: fetch__all__, test_backend_specification
- Classes: TestImportStructures

## temp_repo_analysis\transformers\tests\utils\test_import_utils.py
- Functions: test_clear_import_cache

## temp_repo_analysis\transformers\tests\utils\test_logging.py
- Functions: test_set_progress_bar_enabled
- Classes: HfArgumentParserTest

## temp_repo_analysis\transformers\tests\utils\test_masking_utils.py
- Classes: MaskTest

## temp_repo_analysis\transformers\tests\utils\test_model_card.py
- Classes: ModelCardTester

## temp_repo_analysis\transformers\tests\utils\test_model_debugging_utils.py

## temp_repo_analysis\transformers\tests\utils\test_model_output.py
- Classes: ModelOutputSubclassTester, ModelOutputTest, ModelOutputTestNoDataclass, ModelOutputTester

## temp_repo_analysis\transformers\tests\utils\test_modeling_rope_utils.py
- Classes: RopeTest

## temp_repo_analysis\transformers\tests\utils\test_modeling_utils.py
- Functions: check_models_equal
- Classes: AttentionMaskTester, ModelOnTheFlyConversionTester, ModelPushToHubTester, ModelUtilsTest, TestAttentionImplementation, TestGammaBetaNorm, TestModelGammaBeta, TestSaveAndLoadModelWithExtraState, TestTensorSharing

## temp_repo_analysis\transformers\tests\utils\test_offline.py
- Classes: OfflineTests

## temp_repo_analysis\transformers\tests\utils\test_skip_decorators.py
- Functions: check_slow, check_slow_torch_accelerator, check_slow_torch_cuda, test_pytest_2_skips_slow_first, test_pytest_2_skips_slow_last, test_pytest_param_slow_first, test_pytest_param_slow_last
- Classes: SkipTester

## temp_repo_analysis\transformers\tests\utils\test_tokenization_utils.py
- Classes: ExtensionsTrieTest, TokenizerPushToHubTester, TokenizerUtilTester, TrieTest

## temp_repo_analysis\transformers\tests\utils\test_versions_utils.py
- Classes: DependencyVersionCheckTest

## temp_repo_analysis\transformers\tests\utils\test_video_utils.py
- Functions: get_random_video
- Classes: BaseVideoProcessorTester, LoadVideoTester

## temp_repo_analysis\transformers\utils\add_dates.py
- Functions: get_all_model_cards, get_first_commit_date, get_modified_cards, get_paper_link, get_release_date, insert_dates, main, replace_paper_links

## temp_repo_analysis\transformers\utils\add_pipeline_model_mapping_to_test.py
- Functions: add_pipeline_model_mapping, add_pipeline_model_mapping_to_test_file, find_block_ending, find_test_class, get_framework, get_mapping_for_task, get_model_for_pipeline_test, get_pipeline_model_mapping, get_pipeline_model_mapping_string, is_valid_test_class

## temp_repo_analysis\transformers\utils\check_bad_commit.py
- Functions: create_script, find_bad_commit, get_commit_info

## temp_repo_analysis\transformers\utils\check_build.py
- Functions: test_custom_files_are_present

## temp_repo_analysis\transformers\utils\check_config_attributes.py
- Functions: check_attribute_being_used, check_config_attributes, check_config_attributes_being_used

## temp_repo_analysis\transformers\utils\check_config_docstrings.py
- Functions: check_config_docstrings_have_checkpoints, get_checkpoint_from_config_class

## temp_repo_analysis\transformers\utils\check_copies.py
- Functions: _is_definition_header_ending_line, _sanity_check_splits, _should_continue, check_codes_match, check_copies, check_full_copies, convert_to_localized_md, find_block_end, find_code_and_splits, find_code_in_transformers, get_indent, get_model_list, is_copy_consistent, replace_code, run_ruff, split_code_into_blocks, stylify

## temp_repo_analysis\transformers\utils\check_doc_toc.py
- Functions: check_model_doc, clean_model_doc_toc

## temp_repo_analysis\transformers\utils\check_docstrings.py
- Functions: _find_docstring_end_line, _find_sig_line, check_auto_docstrings, check_docstrings, eval_math_expression, eval_node, find_custom_args_with_details, find_files_with_auto_docstring, find_indent, find_matching_model_files, find_source_file, fix_docstring, generate_new_docstring_for_class, generate_new_docstring_for_function, generate_new_docstring_for_signature, get_args_in_dataclass, get_args_in_signature, get_auto_docstring_candidate_lines, get_default_description, match_docstring_with_signature, replace_default_in_arg_description, stringify_default, update_file_with_new_docstrings

## temp_repo_analysis\transformers\utils\check_doctest_list.py
- Functions: clean_doctest_list

## temp_repo_analysis\transformers\utils\check_dummies.py
- Functions: check_dummies, create_dummy_files, create_dummy_object, find_backend, read_init

## temp_repo_analysis\transformers\utils\check_inits.py
- Functions: analyze_results, check_submodules, find_backend, get_transformers_submodules, parse_init

## temp_repo_analysis\transformers\utils\check_model_tester.py

## temp_repo_analysis\transformers\utils\check_modular_conversion.py
- Functions: compare_files, get_models_in_diff, guaranteed_no_diff, process_file

## temp_repo_analysis\transformers\utils\check_pipeline_typing.py
- Functions: main

## temp_repo_analysis\transformers\utils\check_repo.py
- Functions: check_all_auto_mapping_names_in_config_mapping_names, check_all_auto_mappings_importable, check_all_auto_object_names_being_defined, check_all_decorator_order, check_all_models_are_auto_configured, check_all_models_are_tested, check_all_objects_are_documented, check_decorator_order, check_deprecated_constant_is_up_to_date, check_missing_backends, check_model_list, check_model_type_doc_match, check_models_are_auto_configured, check_models_are_in_init, check_models_are_tested, check_objects_being_equally_in_main_init, check_public_method_exists, check_repo_quality, find_all_documented_objects, find_tested_models, get_all_auto_configured_models, get_model_modules, get_model_test_files, get_models, ignore_unautoclassed, ignore_undocumented, is_a_private_model, is_building_block, should_be_tested

## temp_repo_analysis\transformers\utils\check_self_hosted_runner.py
- Functions: get_runner_status

## temp_repo_analysis\transformers\utils\check_tf_ops.py
- Functions: onnx_compliancy

## temp_repo_analysis\transformers\utils\collated_reports.py
- Functions: get_arguments, get_commit_hash, get_gpu_name, parse_short_summary_line, simplify_gpu_name, upload_collated_report, validate_path
- Classes: Args

## temp_repo_analysis\transformers\utils\compare_test_runs.py
- Functions: compare_job_sets, normalize_test_line, parse_summary_file

## temp_repo_analysis\transformers\utils\create_dependency_mapping.py
- Functions: extract_classes_and_imports, find_priority_list, map_dependencies, topological_sort

## temp_repo_analysis\transformers\utils\create_dummy_models.py
- Functions: build, build_composite_models, build_failed_report, build_model, build_processor, build_simple_report, build_tiny_model_summary, convert_feature_extractor, convert_processors, convert_tokenizer, create_tiny_models, fill_result_with_error, get_architectures_from_config_class, get_checkpoint_dir, get_config_class_from_processor_class, get_config_overrides, get_processor_types_from_config_class, get_tiny_config, get_token_id_from_tokenizer, update_tiny_model_summary_file, upload_model

## temp_repo_analysis\transformers\utils\custom_init_isort.py
- Functions: get_indent, ignore_underscore_and_lowercase, sort_imports, sort_imports_in_all_inits, sort_objects, sort_objects_in_import, split_code_in_indented_blocks

## temp_repo_analysis\transformers\utils\deprecate_models.py
- Functions: add_models_to_deprecated_models_in_config_auto, build_tip_message, delete_model_tests, deprecate_models, extract_model_info, get_last_stable_minor_release, get_line_indent, get_model_doc_path, insert_tip_to_model_doc, move_model_files_to_deprecated, remove_copied_from_statements, remove_model_config_classes_from_config_check, remove_model_references_from_file, update_main_init_file, update_relative_imports

## temp_repo_analysis\transformers\utils\download_glue_data.py
- Functions: download_and_extract, download_diagnostic, format_mrpc, get_tasks, main

## temp_repo_analysis\transformers\utils\extract_pr_number_from_circleci.py

## temp_repo_analysis\transformers\utils\extract_warnings.py
- Functions: extract_warnings, extract_warnings_from_single_artifact

## temp_repo_analysis\transformers\utils\fetch_hub_objects_for_ci.py

## temp_repo_analysis\transformers\utils\get_ci_error_statistics.py
- Functions: download_artifact, get_all_errors, get_artifacts_links, get_errors_from_single_artifact, get_job_links, get_jobs, get_model, make_github_table, make_github_table_per_model, reduce_by_error, reduce_by_model

## temp_repo_analysis\transformers\utils\get_github_job_time.py
- Functions: extract_time_from_single_job, get_job_time

## temp_repo_analysis\transformers\utils\get_modified_files.py

## temp_repo_analysis\transformers\utils\get_pr_run_slow_jobs.py
- Functions: check_name, get_jobs, get_jobs_to_run, parse_message

## temp_repo_analysis\transformers\utils\get_previous_daily_ci.py
- Functions: get_daily_ci_runs, get_last_daily_ci_artifacts, get_last_daily_ci_reports, get_last_daily_ci_run, get_last_daily_ci_run_commit, get_last_daily_ci_workflow_run_id

## temp_repo_analysis\transformers\utils\get_runner_map.py

## temp_repo_analysis\transformers\utils\get_test_info.py
- Functions: get_model_classes, get_model_tester_from_test_class, get_model_to_test_mapping, get_model_to_tester_mapping, get_module_path, get_test_classes, get_test_classes_for_model, get_test_module, get_test_to_tester_mapping, get_tester_classes, get_tester_classes_for_model, to_json

## temp_repo_analysis\transformers\utils\models_to_deprecate.py
- Functions: _extract_commit_hash, get_list_of_models_to_deprecate, get_list_of_repo_model_paths
- Classes: HubModelLister

## temp_repo_analysis\transformers\utils\modular_model_converter.py
- Functions: SUPER_CALL_NODE, append_new_import_node, augmented_dependencies_for_class_node, check_dependencies_and_create_import_node, common_partial_suffix, convert_modular_file, create_modules, dependencies_for_class_node, find_all_dependencies, find_file_type, get_cased_name, get_class_node_and_dependencies, get_full_attribute_name, get_lowercase_name, get_module_source_from_name, get_needed_imports, is_call_to_super, preserve_case_replace, replace_class_node, run_ruff, save_modeling_file, split_all_assignment
- Classes: ClassDependencyMapper, ModelFileMapper, ModularFileMapper, ModuleMapper, ReplaceMethodCallTransformer, ReplaceNameTransformer, SuperTransformer

## temp_repo_analysis\transformers\utils\notification_service.py
- Functions: dicts_to_sum, handle_stacktraces, handle_test_results, pop_default, prepare_reports, retrieve_artifact, retrieve_available_artifacts
- Classes: Message

## temp_repo_analysis\transformers\utils\notification_service_doc_tests.py
- Functions: extract_first_line_failure, handle_test_results, retrieve_artifact, retrieve_available_artifacts
- Classes: Message

## temp_repo_analysis\transformers\utils\past_ci_versions.py

## temp_repo_analysis\transformers\utils\patch_helper.py
- Functions: checkout_branch, cherry_pick_commit, commit_in_history, get_commit_timestamp, get_prs_by_label, get_release_branch_name, main

## temp_repo_analysis\transformers\utils\pr_slow_ci_models.py
- Functions: check_model_names, get_models, get_new_model, get_new_python_files, get_new_python_files_between_commits, parse_message

## temp_repo_analysis\transformers\utils\print_env.py

## temp_repo_analysis\transformers\utils\process_bad_commit_report.py

## temp_repo_analysis\transformers\utils\process_circleci_workflow_test_reports.py

## temp_repo_analysis\transformers\utils\process_test_artifacts.py
- Functions: compute_parallel_nodes, count_lines, process_artifacts

## temp_repo_analysis\transformers\utils\release.py
- Functions: get_version, global_version_update, post_release_work, pre_release_work, remove_conversion_scripts, update_version_in_examples, update_version_in_file

## temp_repo_analysis\transformers\utils\scan_skipped_tests.py
- Functions: _extract_reason_from_decorators, build_model_overrides, extract_test_info, get_common_tests, get_models_and_test_files, main, save_json, summarize_all_tests, summarize_single_test

## temp_repo_analysis\transformers\utils\set_cuda_devices_for_ci.py

## temp_repo_analysis\transformers\utils\sort_auto_mappings.py
- Functions: sort_all_auto_mappings, sort_auto_mapping

## temp_repo_analysis\transformers\utils\split_doctest_jobs.py

## temp_repo_analysis\transformers\utils\split_model_tests.py

## temp_repo_analysis\transformers\utils\test_module\__init__.py

## temp_repo_analysis\transformers\utils\test_module\custom_configuration.py
- Classes: CustomConfig

## temp_repo_analysis\transformers\utils\test_module\custom_feature_extraction.py
- Classes: CustomFeatureExtractor

## temp_repo_analysis\transformers\utils\test_module\custom_image_processing.py
- Classes: CustomImageProcessor

## temp_repo_analysis\transformers\utils\test_module\custom_modeling.py
- Classes: CustomModel

## temp_repo_analysis\transformers\utils\test_module\custom_pipeline.py
- Functions: softmax
- Classes: PairClassificationPipeline

## temp_repo_analysis\transformers\utils\test_module\custom_processing.py
- Classes: CustomProcessor

## temp_repo_analysis\transformers\utils\test_module\custom_tokenization.py
- Classes: CustomTokenizer

## temp_repo_analysis\transformers\utils\test_module\custom_tokenization_fast.py
- Classes: CustomTokenizerFast

## temp_repo_analysis\transformers\utils\test_module\custom_video_processing.py
- Classes: CustomVideoProcessor

## temp_repo_analysis\transformers\utils\tests_fetcher.py
- Functions: _print_list, checkout_commit, clean_code, create_module_to_test_map, create_reverse_dependency_map, create_reverse_dependency_tree, create_test_list_from_filter, diff_contains_doc_examples, diff_is_docstring_only, extract_imports, filter_tests, get_all_doctest_files, get_all_tests, get_diff, get_diff_for_doctesting, get_doctest_files, get_impacted_files_from_tiny_model_summary, get_modified_python_files, get_module_dependencies, get_new_doctest_files, get_tree_starting_at, infer_tests_to_run, init_test_examples_dependencies, keep_doc_examples_only, parse_commit_message, print_tree_deps_of

## temp_repo_analysis\transformers\utils\update_metadata.py
- Functions: camel_case_split, check_pipeline_tags, get_frameworks_table, update_metadata, update_pipeline_and_auto_class_table

## temp_repo_analysis\transformers\utils\update_tiny_models.py
- Functions: get_all_model_names, get_tiny_model_names_from_repo, get_tiny_model_summary_from_hub
